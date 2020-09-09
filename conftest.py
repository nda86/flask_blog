import pytest
from webapp import create_app, db
from webapp.auth.models import User, Role


@pytest.fixture()
def app():
	app = create_app()
	yield app


@pytest.fixture()
def client():
	app = create_app('app_config.TestConfig')
	client = app.test_client()
	db.app = app
	db.create_all()
	yield client
	db.drop_all()


@pytest.fixture()
def create_test_user():
	test_role = Role('default')
	try:
		db.session.add(test_role)
		db.session.commit()
	except Exception:
		db.session.rollback()
		raise

	test_user = User('test')
	test_user.password = '12345678'

	try:
		db.session.add(test_user)
		db.session.commit()
	except Exception:
		db.session.rollback()
		raise
