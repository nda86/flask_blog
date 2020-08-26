import os

from flask import Flask


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

	return app

