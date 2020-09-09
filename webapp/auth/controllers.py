from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify
from flask_login import login_user, logout_user, current_user
from flask_jwt_extended import create_access_token
from requests import HTTPError
from requests_oauthlib import OAuth2Session

from webapp.strings import Title
from webapp import login_manager, db, get_logger
from .forms import RegistrationForm, LoginForm
from .models import User
from app_config import OAuthConfig

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth', template_folder="../templates/auth")

# получаем инстанс логгера
logger = get_logger("auth")

# устанавливаем имя вьюхи, куда будет редиректить незареганных юхзеров при доступе к контенту только для зареганых)
login_manager.login_view = "auth.login"


@login_manager.user_loader
def user_loader(id):
	"""функция для загрузки юзера по его id из бд, если в сессии есть идентификатор залогиненного пользователя"""
	return User.query.get(id)


def get_oauth(state=None, token=None):
	if state:
		return OAuth2Session(client_id=OAuthConfig.CLIENT_ID, redirect_uri=OAuthConfig.REDIRECT_URI, state=state)

	if token:
		return OAuth2Session(client_id=OAuthConfig.CLIENT_ID, token=token)

	return OAuth2Session(client_id=OAuthConfig.CLIENT_ID, redirect_uri=OAuthConfig.REDIRECT_URI, scope=OAuthConfig.SCOPE)


@auth_blueprint.route('/',)
@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
	"""
	маршрут для выполнения входа в систему, сюда же будут перенаправляться запросы требующие регистрации
	:return: html страница входа в систему
	"""
	form = LoginForm()

	# выполняется если на данный урл пришел post запрос и форма прошла валидацию
	if form.validate_on_submit():
		# валидация прошла, логи и пароль верны, следовательно проводим login_user
		user =User.query.filter_by(username=form.username.data).first()
		login_user(user)
		# logger.debug(f"user {user.username} loggin")
		return redirect(url_for('blog.list_posts'))

	# создаем объект для работы с OAuth
	oauth = get_oauth()
	# генерируем ссылку для регистраци по OAuth и state - уникальный код для идентификации, типа csrf
	url, state = oauth.authorization_url(OAuthConfig.AUTH_URI)
	session['state'] = state

	# выполняется если на данный урл пришел get запрос
	return render_template("auth_login.html", title=Title.tLoginPage, form=form, oauth_google_login=url)


@auth_blueprint.route('/gCallback')
def oauth_login():
	"""обработка ответа от провайдера oauth"""

	# если залогиненый юзер зашел на урл, то перенаправляем его
	if current_user.is_authenticated:
		return redirect(url_for("blog.list_posts"))

	# если от провайдера пришли ошибки то пишем их и редиректим на страницу логина
	if 'error' in request.args:
		error = request.args.get('error')
		logger.error(error)
		return redirect(url_for("auth.login"))

	# если в ответе нет ни state ни code значит регистраци не прошла, перенаправляем на стр логина
	if "code" not in request.args and "state" not in request.args:
		return redirect(url_for("auth.login"))
	else:
		# получаем access token
		token = get_oauth(state=session["state"]).fetch_token(OAuthConfig.TOKEN_URI, client_secret=OAuthConfig.CLIENT_SECRET,
														  authorization_response=request.url)
		try:
			request_user_info = get_oauth(token=token).get(OAuthConfig.USER_INFO)
		except HTTPError as e:
			logger.error('server error')
			return redirect(url_for("auth.login"))

		if request_user_info.status_code == 200:
			user_info = request_user_info.json()
			user_email = user_info['email']
			user = User.query.filter_by(username=user_email).first()
			if not user:
				user = User(user_email)
				try:
					db.session.add(user)
					db.session.commit()
				except Exception as e:
					print(e)
					db.session.rollback()
					return redirect(url_for("auth.login"))
				else:
					login_user(user)
					logger.debug(f"User {user.username} have been logged with google. His a new user")
			else:
				login_user(user)
				logger.debug(f"User {user.username} have been logged with google. His alrerady have ben register")
				return redirect(url_for("blog.list_posts"))
		else:
			print('server error')
			return redirect(url_for("auth.login"))


@auth_blueprint.route('/registration', methods=['GET', 'POST'])
def registration():
	"""
	маршрут для выполнения регистрации пользователя в системе
	:return: html страница входа в систему
	"""
	form = RegistrationForm()

	# выполняется если на данный урл пришел post запрос и форма прошла валидацию
	if form.validate_on_submit():
		# так как валидация прошла, можно создавать пользователя
		user = User()
		user.username = form.username.data
		user.password = form.password.data

		try:
			db.session.add(user)
			db.session.commit()
			login_user(user)
			logger.debug(f"User {user} success register!")

			return redirect(url_for('blog.list_posts'))
		except Exception as e:
			logger.error(e)
			db.session.rollback()

	# выполняется если на данный урл пришел get запрос
	return render_template("auth_registration.html", title=Title.tRegistrationPage, form=form)


@auth_blueprint.route('/logout')
def logout():
	logger.debug(f"User {current_user.username} has been loguot")
	logout_user()
	return redirect(url_for('blog.home'))


def authenticate(username, password):
	user = User.query.filter_by(username=username).first()
	if not user:
		return None
	check_password = user.check_password(password)
	if not check_password:
		return None
	return user


# генерация jwt тщкена для доступа к данным по api
@auth_blueprint.route('/api', methods=["POST"])
def api():
	args = request.json
	if not args:
		return jsonify(message="JSON is missing")
	username = args.get("username", None)
	password = args.get("password", None)

	if not username or not password:
		return jsonify(message="Both username and password required")

	user = authenticate(username, password)
	if not user:
		return jsonify(message="Wrong username or password")
	jwt_token = create_access_token(user.id)
	return jsonify(jwt_token=jwt_token)