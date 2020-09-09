from webapp import db, create_app
from webapp.blog.models import Post

app = create_app()

with app.app_context():
	posts = Post.query.order_by(Post.created_at.desc()).all()
	for post in posts:
		print(post.created_at)