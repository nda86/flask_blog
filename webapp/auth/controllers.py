from flask import Blueprint, render_template
from flask_login import login_user, logout_user

from webapp.strings import Title
from webapp import login_manager
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
	return render_template("auth_login.html", title=Title.tLoginPage)

