import pytest
from webapp import create_app


@pytest.fixture()
def app():
	app = create_app()
	yield app


@pytest.fixture()
def client():
	client = create_app().test_client()
	yield client
