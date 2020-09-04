from webapp.strings import Title
import pytest


# @pytest.mark.run(order=2)
def test_registration(client):
	"""Тестирование регистрации пользователя"""

	# тест что страница регистрации доступна
	r = client.get('/auth/registration')
	assert r.status_code == 200
	assert f'<title>{Title.tRegistrationPage}</title>'.encode() in r.data

	# тест на валидацию confirm_password пользователя
	r = client.post('/auth/registration', data=dict(username="test", password="12345678", confirm_password="012345678"), follow_redirects=True)
	assert r.status_code == 200
	assert "Field must be equal to" in r.data.decode('utf-8')

	# тест на успешную регистрацию
	r = client.post('/auth/registration', data=dict(username="test", password="12345678", confirm_password="12345678"), follow_redirects=True)
	assert r.status_code == 200
	assert "test</title>" in r.data.decode('utf-8')

	# тест на проверку свободного имени пользователя
	r = client.post('/auth/registration', data=dict(username="test", password="12345678", confirm_password="12345678"), follow_redirects=True)
	assert r.status_code == 200
	assert "This username is already busy" in r.data.decode('utf-8')


# @pytest.mark.run(order=1)
def test_login_logut(client, create_test_user):
	"""Тестирование входа пользователя"""

	# тест что страница входа доступна
	r = client.get('/auth/login')
	assert r.status_code == 200
	assert f'<title>{Title.tLoginPage}</title>'.encode() in r.data

	# тест на ошибку входа по неверному паролю
	r = client.post('/auth/login', data={'username': 'test', 'password': 'wrongpassword'}, follow_redirects=True)
	assert r.status_code == 200
	assert "Invalid username or password" in r.data.decode('utf-8')

	# тест успешного входа пользователя
	r = client.post('/auth/login', data=dict(username="test", password="12345678"), follow_redirects=True)
	assert r.status_code == 200
	assert "test</title>" in r.data.decode('utf-8')

	# тест выхода пользователя из системы
	r = client.get('/auth/logout', follow_redirects=True)
	assert r.status_code == 200
	assert "test</title>" not in r.data.decode('utf-8')


if __name__ == "__main__":
	pytest.main()
