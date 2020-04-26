import pytest

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


@pytest.fixture(params=SIGN_UP_USERS_VALID_DATA)
def sign_up_users_valid_data(request):
    return request.param


@pytest.fixture(params=SIGN_UP_USERS_INVALID_DATA)
def sign_up_users_invalid_data(request):
    return request.param
