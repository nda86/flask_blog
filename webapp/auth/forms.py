from flask_wtf import FlaskForm as Form
from flask_wtf import RecaptchaField
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo

from .models import User


class RegistrationForm(Form):
	"""
	класс формы регистрации, служит для валидации введенных данных
	"""
	username = StringField("Login", validators=[DataRequired(), Length(max=50)])
	password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
	confirm_password = PasswordField("Подтверждение пароля", validators=[DataRequired("Поле обязательно для заполнения!"), EqualTo('password')])
	recaptha = RecaptchaField()

	def validate(self):
		"""
		Сначала проводим основную валидацию, по указанным валидаторам, а потом проверяем не занято ли username бд
		:return:
		"""
		main_valid = super().validate()

		if not main_valid:
			# не забываем добавить form.hidden_tag() в шаблон, чтобы разместить на форме csrf токен
			# без этого валидация не будет проходить, и ошибок не увидите
			return False

		user = User.query.filter_by(username=self.username.data.lower()).first()
		if user:
			self.username.errors.append('This username is already busy')
			return False

		return True


class LoginForm(Form):
	"""
	форма логина пользователя, проводит валидацию на заполненность полей,
	потом ищет пользователя в бд по имени, если его нет то возврат False
	если такой пользователь есть то проверяет введенный пароль, с паролем в бд(по хешу)
	если пароль не верен то возврат False
	если всё гуд, то True
	важно: не пишем отдельно что пользователь не найден или что пароль не верен, это не безопасно!
	в обоих случаях просто пишем "Wrong username or password"!
	"""
	username = StringField("Login", validators=[DataRequired()])
	password = PasswordField("Password", validators=[DataRequired()])
	recaptcha = RecaptchaField()

	def validate(self):
		main_valid = super().validate()

		if not main_valid:
			return False

		user = User.query.filter_by(username=self.username.data.lower()).first()

		if not user:
			self.username.errors.append('Invalid username or password')
			return False

		check_password = user.check_password(self.password.data)

		if not check_password:
			self.username.errors.append('Invalid username or password')
			return False

		return True
