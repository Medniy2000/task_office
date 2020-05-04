import uuid

from flask import url_for

from tests.factories import USER_FACTORY_DEFAULT_PASSWORD


def test_sign_up_success(testapp, sign_up_users_valid_data):
    url = url_for("api_v1.sign_up")
    testapp.post_json(url, sign_up_users_valid_data, status=200)


def test_sign_up_failed(testapp, sign_up_users_invalid_data):
    url = url_for("api_v1.sign_up")
    testapp.post_json(url, sign_up_users_invalid_data, status=422)


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


def test_sign_up_in_success(testapp, sign_up_users_valid_data):
    # sign up
    sign_up_url = url_for("api_v1.sign_up")
    testapp.post_json(sign_up_url, sign_up_users_valid_data, status=200)

    # sign in
    sign_in_url = url_for("api_v1.sign_in")
    data = {
        "email": sign_up_users_valid_data["email"],
        "password": sign_up_users_valid_data["password"],
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


def test_refresh_failed(testapp, refresh_users_invalid_data):
    url = url_for("api_v1.refresh",)
    headers = {"Authorization": f"Bearer {refresh_users_invalid_data}"}
    testapp.post_json(url, headers=headers, status=422)
