from flask import Blueprint, render_template
from flask_login import login_required, current_user

from webapp.strings import Title
from .models import Post, Tag
from webapp import get_logger


blog_blueprint = Blueprint('blog', __name__, url_prefix='/blog', template_folder='../templates/blog')
logger = get_logger("blog")

@blog_blueprint.route('/')
def home():
	return render_template("blog_home.html", title='Home | Blog')


@blog_blueprint.route('/posts', methods=['GET', 'POST'])
@login_required
def list_posts():
	logger.debug(f"User {current_user.username} has access to the blog page")
	posts = Post.query.order_by(Post.created_at.desc()).all()
	return render_template("blog_posts.html", title=Title.tBlogPosts, posts=posts)