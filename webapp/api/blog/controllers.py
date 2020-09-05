from flask_restful import Resource, marshal_with
from flask_jwt_extended import jwt_required
from webapp.blog.models import Post
from .fields import get_post_field


class BlogApi(Resource):
	@marshal_with(get_post_field)
	@jwt_required
	def get(self):
		posts = Post.query.all()
		return posts
