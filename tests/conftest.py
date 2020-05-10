import pytest
from flask import url_for
from webtest import TestApp

from task_office.app import create_app
from task_office.extensions.db import db as _db
from task_office.settings import app_config
from tests.factories import USER_FACTORY_DEFAULT_PASSWORD


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


@pytest.fixture(scope="function")
def auth_user(func_users, testapp):
    sign_in_url = url_for("api_v1.sign_in")
    user = func_users.get_single()
    data = {
        "email": user.email,
        "password": USER_FACTORY_DEFAULT_PASSWORD,
    }
    resp = testapp.post_json(sign_in_url, data, status=200)
    return {"current_user": user, "auth_data": resp.json}


pytest_plugins = [
    "tests.fixtures.model_fixtures",
    "tests.unit.app.core.fixtures",
    "tests.integration.app.auth.fixtures",
    "tests.integration.app.boards.fixtures",
    "tests.integration.app.columns.fixtures",
    "tests.integration.app.tasks.fixtures",
    "tests.integration.app.permissions.fixtures",
]
