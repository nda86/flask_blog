class BaseConfig(object):
	pass


class DevConfig(BaseConfig):
	DEBUG = True

	SECRET_KEY = "thisisasecret"

	SQLALCHEMY_DATABASE_URI = "sqlite:///webapp.sqlite3"
	SQLALCHEMY_ECHO = True
	SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(BaseConfig):
	pass
