from webapp import create_app


def test_create_app():
	"""тест работы фабрики приложения Flask
	если не указан файл конфигурации, то должен создаваться app с конфигом по умолчанию
	иначе с переданным конфигом
	"""
	assert not create_app().testing
	assert create_app('webapp.tests.config.TestConfig').testing
