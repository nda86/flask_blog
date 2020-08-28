import os

from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from .strings import Title

# объект класса flask-sqlalchemy - ORM
db = SQLAlchemy()
# объект для вывполнения миграций бд
migrate = Migrate()
# объект для хеширования паролей пользователей
bcrypt = Bcrypt()
# логин менеджер для, используем для работы с пользователями
login_manager = LoginManager()


def error_404(error):
	"""
	обработчик для 404 ошибки
	:return: html страница для 404 ошибки
	"""
	return render_template("404.html", title=Title.t404), 404


def error_500(error):
	"""
	обработчик для 500 ошибки
	:return: html страница для 500 ошибки
	"""
	return render_template("500.html", title=Title.t500), 500


def create_app(config=None):
	"""
	фабрика для создания инстанса сервера flask
	:param config: полный путь к классу конфигурации(example: app_config.DevConfig or app_config.ProdConfig)
	в виде строки или ссылка на объект класса конфигурации, предварительно его нужно импортировать
	:return: app - инстанс класса Flask - экземпляр сервера
	"""

	app = Flask(__name__)

	# если имя или путь к классу конфигурации не передан, то загружаем файл конфигурации в зависимости
	# от переменной окружения ENV, её дефолтное значение устанавливаем в 'dev'
	config = config or f"app_config.{os.environ.get('ENVIROMENT', 'dev').capitalize()}Config"
	app.config.from_object(config)

	# инициализируем flask extensions

	# инициализируем бд
	db.init_app(app)

	# инициализирууем миграцию
	# для sqlite db нужно дополнительно указывать параметр render_as_batch=True,
	# для выполнения ALTER TABLE ADD COLUMN | ALTER TABLE REMOVE COLUMN | ALTER TABLE RENAME COLUMN | ALTER TABLE RENAME
	# поэтому сначала определим является ли используемая бд sqlite db
	# так же ставим параметр compare_type=True, чтобы при создании миграции учитывались изменения типов полей таблицы
	with app.app_context():
		is_sqlite = db.engine.url.drivername == 'sqlite'
	migrate.init_app(app, db, render_as_batch=is_sqlite, compare_type=True)

	# инициализируем утилиту для создания и проверки хешей паролей
	bcrypt.init_app(app)

	# для выполнения входа пользователя в систему, выхода и определения текущего пользователя
	login_manager.init_app(app)

	# импотируем функцию регистрации блюпринта и передаем в ней app, таким образом добавляем модуль(блюпринт) к серверу
	from .blog import create_module as create_blog
	from .auth import create_module as create_auth

	create_blog(app)
	create_auth(app)

	# регистрируем обработчики ошибок
	app.register_error_handler(404, error_404)
	app.register_error_handler(500, error_500)

	# маршрут-заглушка
	# редирект с корня сайта на главную страницу блога
	@app.route("/")
	def index():
		return redirect('/blog')

	return app


