import uuid

import pytest
import webtest
from flask import url_for

from tests.factories import USER_FACTORY_DEFAULT_PASSWORD


def test_sign_up_success(testapp, valid_sign_up_users_valid_data):
    url = url_for("api_v1.sign_up")
    resp = testapp.post_json(url, valid_sign_up_users_valid_data)
    assert resp.status == "200 OK"


def test_sign_up_failed(testapp, valid_sign_up_users_invalid_data):
    url = url_for("api_v1.sign_up")
    with pytest.raises(webtest.app.AppError):
        resp = testapp.post_json(url, valid_sign_up_users_invalid_data)
        assert "422 UNPROCESSABLE ENTITY" == resp.status


def test_sign_up_already_exists_username(testapp, function_users):
    available_username = function_users.get_single().username

    data = {
        "password_confirm": "user11",
        "password": "user11",
        "email": "user1@gmaill.com",
        "username": available_username,
    }

    url = url_for("api_v1.sign_up")
    with pytest.raises(webtest.app.AppError):
        resp = testapp.post_json(url, data)
        assert "422 UNPROCESSABLE ENTITY" == resp.status


def test_sign_up_already_exists_email(testapp, function_users):
    available_email = function_users.get_single().email

    data = {
        "password_confirm": "user11",
        "password": "user11",
        "email": available_email,
        "username": "user",
    }

    url = url_for("api_v1.sign_up")
    with pytest.raises(webtest.app.AppError):
        resp = testapp.post_json(url, data)
        assert "422 UNPROCESSABLE ENTITY" == resp.status


def test_sign_up_in_success(testapp, valid_sign_up_users_valid_data):
    # sign up
    sign_up_url = url_for("api_v1.sign_up")
    resp = testapp.post_json(sign_up_url, valid_sign_up_users_valid_data)
    assert resp.status == "200 OK"

    # sign in
    sign_in_url = url_for("api_v1.sign_in")
    data = {
        "email": valid_sign_up_users_valid_data["email"],
        "password": valid_sign_up_users_valid_data["password"],
    }
    resp = testapp.post_json(sign_in_url, data)
    assert resp.status == "200 OK"


def test_sign_in_data__with_valid_data(testapp, function_users):
    sign_in_url = url_for("api_v1.sign_in")
    data = {
        "email": function_users.get_single().email,
        "password": USER_FACTORY_DEFAULT_PASSWORD,
    }
    resp = testapp.post_json(sign_in_url, data)
    assert resp.status == "200 OK"


def test_sign_in_data_with_invalid_data(testapp,):
    sign_in_url = url_for("api_v1.sign_in")
    with pytest.raises(webtest.app.AppError):
        data = {
            "email": f"user{uuid.uuid4().hex}@gmail.com",
            "password": "some_wrong_password",
        }
        resp = testapp.post_json(sign_in_url, data)
        assert resp.status == "422 UNPROCESSABLE ENTITY"


def test_sign_in_data_with_invalid_email(testapp, function_users):
    sign_in_url = url_for("api_v1.sign_in")
    with pytest.raises(webtest.app.AppError):
        data = {
            "email": "user{}@gmail.com".format(uuid.uuid4().hex),
            "password": USER_FACTORY_DEFAULT_PASSWORD,
        }
        resp = testapp.post_json(sign_in_url, data)
        assert resp.status == "422 UNPROCESSABLE ENTITY"


def test_sign_in_data__with_invalid_password(testapp, function_users):
    sign_in_url = url_for("api_v1.sign_in")
    with pytest.raises(webtest.app.AppError):
        data = {
            "email": function_users.get_single().email,
            "password": "some_wrong_password",
        }
        resp = testapp.post_json(sign_in_url, data)
        assert resp.status == "422 UNPROCESSABLE ENTITY"
