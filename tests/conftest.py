import pytest


from webtest import TestApp

from eGrader import create_app
from eGrader.core import db
from tests import settings
from tests.factories import UserFactory


@pytest.yield_fixture(scope='function')
def app():
    """An application for the tests."""
    _app = create_app()
    _app.config.from_object(settings)
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope='function')
def test_client(app):
    client = TestApp(app)
    return client


@pytest.yield_fixture(scope='function')
def database(app):
    """The database used for testing"""
    db.app = app
    with app.app_context():
        db.create_all()

    def teardown():
        print('dropping all, maybe?')
        db.drop_all()

    yield db

    db.session.close()
    db.drop_all()


@pytest.fixture
def user(database):
    """A user for the tests"""
    user = UserFactory(password='iH3@r7P1zz@')
    db.session.commit()
    return user
