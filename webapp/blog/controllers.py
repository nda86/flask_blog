from flask import Blueprint, render_template

blog_blueprint = Blueprint('blog', __name__, url_prefix='/blog', template_folder='../templates/blog')


@blog_blueprint.route('/')
def home():
	return render_template("blog_home.html", title='Home | Blog')