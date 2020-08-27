from webapp import db, bcrypt
from flask_login import UserMixin

# вспомогательная таблица, хранит соответствия user и role
roles = db.Table('user_role', db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
					db.Column('role_id', db.Integer, db.ForeignKey('role.id')))


class User(db.Model, UserMixin):
	"""
	Класс определяет таблицу пользователей в бд.
	Каждый пользователь имеет уникальное имя(поле username индексировано, для лучшего поиска по имени в бд.
	"""
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(255), unique=True, nullable=False)
	password = db.Column(db.String(255), nullable=False)
	# имеет связь многие ко многим с таблицей Role.
	roles = db.relationship('Role', secondary=roles, backref=db.backref('users', lazy='dynamic'))
	# имеет связи один ко многим с таблицей Post.
	posts = db.relationship('Post', backref='user', lazy='dynamic')

	# 	Пароль - устанавливаем не напрямую, а через метод set_password, в этом случае вместо пароля в базу
	# 	записывается его хеш.
	def set_password(self, password):
		self.password = bcrypt.generate_password_hash(password)

	# метод для проверки переданного пароля
	# сравниваем с хешем пароля хранимым в бд
	def check_password(self, password):
		return bcrypt.check_password_hash(self.password, password)

	# переопределенный метод класса UserMixin, служит для получения идентификатора пользователя,
	# при выполнении flask_login.login_user
	def get_id(self):
		return self.id

	# метод для определения владеет ли пользователь определенной ролью
	def has_role(self, name):
		for role in self.roles:
			if role == name:
				return True
		return False

	def __init__(self, username=""):
		self.username = username

	def __repr__(self):
		return f"<User {self.username}>"


class Role(db.Model):
	"""
	Класс определяет простую таблицу ролей пользователей
	"""
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255), unique=True)

	def __init__(self, title=""):
		self.title = title

	def __repr__(self):
		return f"<Role {self.title}>"
