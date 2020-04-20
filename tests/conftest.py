import pytest
from webtest import TestApp

from task_office.app import create_app
from task_office.extensions.db import db as _db
from task_office.settings import app_config


@pytest.yield_fixture(scope="function")
def app():
    """An application for the tests."""
    _app = create_app(app_config)

    with _app.app_context():
        _db.create_all()

    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope="function")
def testapp(app):
    """A Webtest app."""
    return TestApp(app)


@pytest.yield_fixture(scope="function")
def db(app):
    """A database for the tests."""
    _db.app = app
    with app.app_context():
        _db.create_all()

    yield _db

    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()


pytest_plugins = [
    "tests.fixtures.model_fixtures",
    "tests.unit.app.core.fixtures",
]
