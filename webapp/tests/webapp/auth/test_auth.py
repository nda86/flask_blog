from webapp.strings import Title


def test_login(client):
	"""Тест что страница логина существует и отдается по заданному урлу"""
	r = client.get('/auth/login')
	assert r.status_code == 200
	assert f'<title>{Title.tLoginPage}</title>'.encode() in r.data
