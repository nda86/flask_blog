from flask import url_for
from flask_admin import Admin
from .controllers import CustomModelView, CustomFileAdmin, back_to_site_link
from webapp import db
from webapp.blog.models import Post, Tag
from webapp.auth.models import User, Role


def create_module(app):

	# создаем экземляр админк, передаем в конструктор ссылку на flask app для инициализации app и flask-admin
	admin = Admin(app, "Flask Blog", template_mode='bootstrap3')

	# список моделей, которые будут управляться через flask-admin
	# в виде [(category, [list of models]), ...]
	models = [
		('Blog', [Post, Tag]),
		('Users', [User, Role])
	]

	# добавляем модели в модуль flask-admin для возможности ими управлять через интерфейс админки
	for model in models:
		for model_name in model[1]:
			admin.add_view(CustomModelView(model_name, session=db.session, category=model[0]))

	# добавляем интерфейс управления статикой
	admin.add_view(CustomFileAdmin(app.static_folder, name='Static Files'))

	# добавляем в меню flask-admin ссылку для возврата на главную страницу блога
	admin.add_menu_item(back_to_site_link)

