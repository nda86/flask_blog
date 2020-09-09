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

	DEBUG_TB_INTERCEPT_REDIRECTS = False
	DEBUG_TB_PROFILER_ENABLED = True


class ProdConfig(BaseConfig):
	DEBUG = False


class TestConfig(BaseConfig):
	DEBUG = True
	TESTING = True

	DEBUG_TB_ENABLED = False

	WTF_CSRF_ENABLED = False

	# SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
	SQLALCHEMY_DATABASE_URI = "sqlite:///webapp_test.sqlite3"
	SQLALCHEMY_TRACK_MODIFICATIONS = False


class OAuthConfig:
	# google
	CLIENT_ID = "555654849421-3ga9efk4vt4tonuhqt5o1v3o52ciidka.apps.googleusercontent.com"
	CLIENT_SECRET = "3wUHf_007O-yP5Ts1350Uv8W"
	REDIRECT_URI = "https://127.0.0.1:5005/auth/gCallback"
	AUTH_URI = "https://accounts.google.com/o/oauth2/auth"
	TOKEN_URI = "https://accounts.google.com/o/oauth2/token"
	USER_INFO = "https://www.googleapis.com/userinfo/v2/me"
	SCOPE = ['email']
