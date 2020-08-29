from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.menu import MenuLink

# создаем сслыку для возврата на сайт из интерфейса flask-admin
back_to_site_link = MenuLink(name='Back to site', endpoint='blog.home')


class CustomModelView(ModelView):
	"""
	класс для переопределения дефолтных настроек по возможностям взаимодействия с управляемым классом
	(по сути таблицей в бд)
	"""
	pass


class CustomFileAdmin(FileAdmin):
	"""
	класс для переопределения настроек интерфейса управления файлами
	"""
	pass
