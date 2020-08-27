from .controllers import auth_blueprint


def create_module(app):
	"""
	функция регистрации блюпринта во flask приложении
	:param app: объект flask приложения
	:return:
	"""
	app.register_blueprint(auth_blueprint)
