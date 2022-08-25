import pytest

from app import create_app
from config import Config
from setup_db import db as database


@pytest.fixture(scope='session')
def app():
    app = create_app(Config)
    with app.app_context():
        yield app


@pytest.fixture(scope='session')
def db(app):
    database.init_app(app)
    database.create_all()
    database.session.commit()

    yield database

    database.session.close()
