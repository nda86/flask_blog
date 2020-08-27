from flask import Blueprint, render_template
from flask_login import login_required

from webapp.strings import Title


blog_blueprint = Blueprint('blog', __name__, url_prefix='/blog', template_folder='../templates/blog')


@blog_blueprint.route('/')
def home():
	return render_template("blog_home.html", title='Home | Blog')


@blog_blueprint.route('/posts', methods=['GET', 'POST'])
@login_required
def posts():
	return render_template("blog_posts.html", title=Title.tBlogPosts)