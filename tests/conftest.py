import pytest

from app import create_app
from app.extensions import db


@pytest.fixture()
def app():
    test_app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    yield test_app

    with test_app.app_context():
        db.session.remove()


@pytest.fixture()
def client(app):
    return app.test_client()