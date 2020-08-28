class BaseConfig(object):
	a = 1
	RECAPTCHA_PRIVATE_KEY = "6LfxHLgZAAAAAPgxhud9_IAGvlI30fUaJO5ePJmf"
	RECAPTCHA_PUBLIC_KEY = "6LfxHLgZAAAAAEgzIgnllFLG9NvPEUYrHgignv17"

	SECRET_KEY = 'secret'


class DevConfig(BaseConfig):
	DEBUG = True

	SECRET_KEY = "thisisasecret"

	SQLALCHEMY_DATABASE_URI = "sqlite:///webapp.sqlite3"
	SQLALCHEMY_ECHO = True
	SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(BaseConfig):
	pass


class TestConfig(BaseConfig):
	DEBUG = True
	TESTING = True

	WTF_CSRF_ENABLED = False

	# SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
	SQLALCHEMY_DATABASE_URI = "sqlite:///webapp_test.sqlite3"
	SQLALCHEMY_TRACK_MODIFICATIONS = False
