from webapp import create_app
import warnings


def test_create_app():
	"""тест работы фабрики приложения Flask
	если не указан файл конфигурации, то должен создаваться app с конфигом по умолчанию
	иначе с переданным конфигом
	"""
	assert not create_app().testing
	# отключаем варнинги, чтоб не было сообщений о незаполнености параметров в конфигурации,
	# так как в этом тесте это не важно
	warnings.filterwarnings('ignore')
	assert create_app('webapp.tests.config.TestConfig').testing
