from webapp import create_app, db
from webapp.auth.models import User, Role
from webapp.blog.models import Post, Tag


app = create_app()


@app.shell_context_processor
def make_ctx():
	return dict(app=app, db=db, User=User, Role=Role, Post=Post, Tag=Tag)
