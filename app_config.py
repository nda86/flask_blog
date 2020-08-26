class BaseConfig(object):
	pass


class DevConfig(BaseConfig):
	DEBUG = True

	SECRET_KEY = "thisisasecret"


class ProdConfig(BaseConfig):
	pass
