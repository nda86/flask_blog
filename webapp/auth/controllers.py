from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_user, logout_user

from webapp.strings import Title
from webapp import login_manager, db
from .forms import RegistrationForm, LoginForm
from .models import User

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth', template_folder="../templates/auth")

# устанавливаем имя вьюхи, куда будет редиректить незареганных юхзеров при доступе к контенту только для зареганых)
login_manager.login_view = "auth.login"


@login_manager.user_loader
def user_loader(id):
	"""функция для загрузки юзера по его id из бд, если в сессии есть идентификатор залогиненного пользователя"""
	return User.query.get(id)


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
		login_user(User.query.filter_by(username=form.username.data).first())
		return redirect(url_for('blog.posts'))

	# выполняется если на данный урл пришел get запрос
	return render_template("auth_login.html", title=Title.tLoginPage, form=form)


@auth_blueprint.route('/register', methods=['GET', 'POST'])
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
		user.set_password(form.password.data)

		try:
			db.session.add(user)
			db.session.commit()
			login_user(user)
			return redirect(url_for('blog.posts'))
		except Exception as e:
			print(e)
			db.session.rollback()

	# выполняется если на данный урл пришел get запрос
	return render_template("auth_registration.html", title=Title.tRegistrationPage, form=form)


@auth_blueprint.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('blog.home'))
