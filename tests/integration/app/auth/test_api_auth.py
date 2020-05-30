import uuid

import pytest
from flask import url_for

from task_office.core.utils import generate_str
from tests.factories import USER_FACTORY_DEFAULT_PASSWORD

SIGN_UP_USERS_VALID_DATA = [
    {
        "password_confirm": "user11",
        "password": "user11",
        "email": "user1@gmaill.com",
        "username": "usr1",
    },
    {
        "password_confirm": "user5678910124556122345811111111",
        "password": "user5678910124556122345811111111",
        "email": "user2@gmaill.com",
        "username": "usr2",
    },
    {
        "password_confirm": "user11",
        "password": "user11",
        "email": "user3@gmaill.com",
        "username": "usr3123456usr3123456usr3123456usr3123456usr3123456usr3123456usr3123456usr3123456",
    },
]


@pytest.mark.parametrize("data", SIGN_UP_USERS_VALID_DATA)
def test_sign_up_success(testapp, data):
    url = url_for("api_v1.sign_up")
    testapp.post_json(url, data, status=200)


SIGN_UP_USERS_INVALID_DATA = [
    # to short password
    {
        "password_confirm": "us",
        "password": "us",
        "email": "user1@gmaill.com",
        "username": "usr1",
    },
    # invalid email
    {
        "password_confirm": "user11",
        "password": "user11",
        "email": "user1gmaill.com",
        "username": "usr1",
    },
    # to short username
    {
        "password_confirm": "user11",
        "password": "user11",
        "email": "user1@gmaill.com",
        "username": "us",
    },
    # to long password
    {
        "password_confirm": "user56789101245561223458111111111",
        "password": "user56789101245561223458111111111",
        "email": "user2@gmaill.com",
        "username": "usr2",
    },
    # to long username
    {
        "password_confirm": "user11",
        "password": "user11",
        "email": "user3@gmaill.com",
        "username": "usr3123456usr3123456usr3123456usr3123456usr3123456usr3123456usr3123456usr31234561",
    },
    # passwords not equal
    {
        "password_confirm": "user12",
        "password": "user11",
        "email": "user3@gmaill.com",
        "username": "usr3123456usr3123456usr3123456usr3123456usr3123456usr3123456usr3123456usr3123456",
    },
]


@pytest.mark.parametrize("data", SIGN_UP_USERS_INVALID_DATA)
def test_sign_up_failed(testapp, data):
    url = url_for("api_v1.sign_up")
    testapp.post_json(url, data, status=422)


def test_sign_up_already_exists_username(testapp, func_users):
    available_username = func_users.get_single().username

    data = {
        "password_confirm": "user11",
        "password": "user11",
        "email": "user1@gmaill.com",
        "username": available_username,
    }

    url = url_for("api_v1.sign_up")
    testapp.post_json(url, data, status=422)


def test_sign_up_already_exists_email(testapp, func_users):
    available_email = func_users.get_single().email

    data = {
        "password_confirm": "user11",
        "password": "user11",
        "email": available_email,
        "username": "user",
    }

    url = url_for("api_v1.sign_up")
    testapp.post_json(url, data, status=422)


@pytest.mark.parametrize("data", SIGN_UP_USERS_VALID_DATA)
def test_sign_up_in_success(testapp, data):
    # sign up
    sign_up_url = url_for("api_v1.sign_up")
    testapp.post_json(sign_up_url, data, status=200)

    # sign in
    sign_in_url = url_for("api_v1.sign_in")
    data = {
        "email": data["email"],
        "password": data["password"],
    }
    testapp.post_json(sign_in_url, data, status=200)


def test_sign_in_data__with_valid_data(testapp, func_users):
    sign_in_url = url_for("api_v1.sign_in")
    data = {
        "email": func_users.get_single().email,
        "password": USER_FACTORY_DEFAULT_PASSWORD,
    }
    testapp.post_json(sign_in_url, data, status=200)


def test_sign_in_data_with_invalid_data(testapp):
    sign_in_url = url_for("api_v1.sign_in")
    data = {
        "email": f"user{uuid.uuid4().hex}@gmail.com",
        "password": "some_wrong_password",
    }
    testapp.post_json(sign_in_url, data, status=422)


def test_sign_in_data_with_invalid_email(testapp):
    sign_in_url = url_for("api_v1.sign_in")
    data = {
        "email": "user{}@gmail.com".format(uuid.uuid4().hex),
        "password": USER_FACTORY_DEFAULT_PASSWORD,
    }
    testapp.post_json(sign_in_url, data, status=422)


def test_sign_in_data__with_invalid_password(testapp, func_users):
    sign_in_url = url_for("api_v1.sign_in")
    data = {
        "email": func_users.get_single().email,
        "password": "some_wrong_password",
    }
    testapp.post_json(sign_in_url, data, status=422)


def test_refresh_success(testapp, auth_user):
    url = url_for("api_v1.refresh",)
    token = auth_user["auth_data"]["tokens"]["refresh"]["token"]
    headers = {"Authorization": f"Bearer {token}"}
    testapp.post_json(url, headers=headers, status=200)


REFRESH_INVALID = [
    "",
    None,
    generate_str(25),
]


@pytest.mark.parametrize("data", REFRESH_INVALID)
def test_refresh_failed(testapp, data):
    url = url_for("api_v1.refresh",)
    headers = {"Authorization": f"Bearer {data}"}
    testapp.post_json(url, headers=headers, status=422)
