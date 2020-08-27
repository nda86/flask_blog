from .controllers import blog_blueprint


def create_module(app):
	app.register_blueprint(blog_blueprint)