from .blog.controllers import BlogApi
from flask_restful import Api


api = Api(prefix="/api/v1")
api.add_resource(BlogApi, "/list_posts")


def create_module(app):
	api.init_app(app)
