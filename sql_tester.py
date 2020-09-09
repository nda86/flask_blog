from webapp import db, create_app
from webapp.blog.models import Post

app = create_app()

with app.app_context():
	posts = Post.query.order_by(Post.created_at.desc()).all()
	print(len(posts))
	pag = Post.query.order_by(Post.created_at.desc()).paginate(3, 5)
	print(pag.prev())