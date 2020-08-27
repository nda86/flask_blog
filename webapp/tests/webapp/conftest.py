import pytest
from flask import render_template
from webapp import create_app
from webapp.strings import Title


@pytest.fixture()
def app():
	app = create_app()
	yield app


@pytest.fixture()
def client():
	client = create_app().test_client()
	yield client

