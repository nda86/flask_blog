import os

from flask import Flask


def create_app(config=None):
	app = Flask(__name__)
	config = config or f"app_config.{os.environ.get('ENVIROMENT', 'dev').capitalize()}Config"
	app.config.from_object(config)

	return app
