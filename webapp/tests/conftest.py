import pytest
from flask import render_template
from webapp import create_app
from ..strings import Title


@pytest.fixture()
def app():
	app = create_app()
	yield app


@pytest.fixture()
def client():
	client = create_app().test_client()
	yield client


@pytest.fixture()
def get_404_page():
	with create_app().app_context():
		yield render_template('404.html', title=Title.t404)


@pytest.fixture()
def get_500_page():
	with create_app().app_context():
		yield render_template('500.html', title=Title.t500)
