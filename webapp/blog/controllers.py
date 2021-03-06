from flask import Blueprint, render_template, current_app, request
from flask_login import login_required, current_user
from webapp import cache
from webapp.strings import Title
from .models import Post, Tag
from webapp import get_logger


blog_blueprint = Blueprint('blog', __name__, url_prefix='/blog', template_folder='../templates/blog')
logger = get_logger("blog")


@blog_blueprint.route('/')
def home():
	return render_template("blog_home.html", title='Home | Blog')


@blog_blueprint.route('/posts', methods=['GET', 'POST'])
@blog_blueprint.route('/posts/<int:page>', methods=['GET', 'POST'])
@login_required
@cache.cached(key_prefix=lambda: f"_{request.path}")
def list_posts(page=None):
	logger.debug(f"User {current_user.username} has access to the blog page")
	page = page or 1
	posts = Post.query.order_by(Post.created_at.desc()).paginate(page=page, per_page=current_app.config.get("POST_PER_PAGE", 5))
	return render_template("blog_posts.html", title=Title.tBlogPosts, posts=posts)
