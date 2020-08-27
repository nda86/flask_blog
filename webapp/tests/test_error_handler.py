import pytest


def test_404(client, get_404_page):
	"""
	тест 404 ошибки
	успех если: код ответа 404 и response.data == 404.html
	:param client: app.test_client() - fixture
	:param get_404_page: отрендеренный ответ 404.html
	:return:
	"""
	r = client.get('/fwewefffefefwefcsdcsdc')
	assert r.status_code == 404
	assert r.data.decode('utf-8') == get_404_page


def _test_500(client, get_500_page):
	"""
	тест 500 ошибки
	успех если: код ответа 500 и response.data == 500.html
	:param client: app.test_client() - fixture
	:param get_500_page: отрендеренный ответ 500.html
	:return:
	"""
	r = client.get('/fwewefffefefwefcsdcsdc')
	assert r.status_code == 500
	assert r.data.decode('utf-8') == get_500_page


if __name__ == "__main__":
	pytest.main(['-vv', '-s'])
