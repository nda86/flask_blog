import os

from flask import Flask, render_template

from .strings import Title


def error_404(error):
	"""
	обработчик для 404 ошибки
	:return:
	"""
	return render_template("404.html", title=Title.t404), 404


def error_500(error):
	"""
	обработчик для 500 ошибки
	:return:
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

	# импотируем функцию регистрации блюпринта и передаем в ней app, таким образом добавляем модуль(блюпринт) к серверу
	from .blog import create_module as create_blog
	create_blog(app)

	# регистрируем обработчики ошибок
	app.register_error_handler(404, error_404)
	app.register_error_handler(500, error_500)

	return app


