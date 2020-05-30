import uuid

import pytest as pytest
from flask import url_for

from task_office.core.utils import generate_str


def test_get_list_boards_without_auth(testapp):
    url = url_for("api_v1.get_list_boards")
    testapp.get(url, status=401)


def test_get_board_without_auth(testapp, func_boards):
    url = url_for(
        "api_v1.get_board", board_uuid=uuid.UUID(func_boards.get_single().uuid).hex
    )
    testapp.get(url, status=401)


def test_get_board_users_without_auth(testapp, func_boards):
    url = url_for(
        "api_v1.get_board_users",
        board_uuid=uuid.UUID(func_boards.get_single().uuid).hex,
    )
    testapp.get(url, status=401)


def test_create_board_without_auth(testapp):
    url = url_for("api_v1.create_board")
    data = {
        "name": "Board # name",
        "description": "Board #3 description",
        "is_active": True,
    }
    testapp.post_json(url, data, status=401)


def test_update_board_without_auth(testapp, func_boards):
    url = url_for(
        "api_v1.update_board", board_uuid=uuid.UUID(func_boards.get_single().uuid).hex,
    )
    data = {
        "name": "Board # name",
        "description": "Board #3 description",
        "is_active": True,
    }
    testapp.put_json(url, data, status=401)


def test_get_boards_list(testapp, auth_user):
    url = url_for("api_v1.get_list_boards")
    token = auth_user["auth_data"]["tokens"]["access"]["token"]
    headers = {"Authorization": f"Bearer {token}"}
    testapp.get(url, headers=headers, status=200)


def test_get_board(testapp, func_boards, auth_user):
    url = url_for(
        "api_v1.get_board", board_uuid=uuid.UUID(func_boards.get_single().uuid).hex
    )
    token = auth_user["auth_data"]["tokens"]["access"]["token"]
    headers = {"Authorization": f"Bearer {token}"}
    testapp.get(url, headers=headers, status=200)


def test_get_board_users(testapp, func_boards, auth_user):
    url = url_for(
        "api_v1.get_board_users",
        board_uuid=uuid.UUID(func_boards.get_single().uuid).hex,
    )
    token = auth_user["auth_data"]["tokens"]["access"]["token"]
    headers = {"Authorization": f"Bearer {token}"}
    testapp.get(url, headers=headers, status=200)


BOARDS_VALID_DATA = [
    # Typical  board data
    {"name": "Board 1# name", "description": "Board #3 description", "is_active": True},
    # Data without is_active
    {"name": "Board 2# name", "description": "Board #3 description"},
    # Data without description
    {"name": "Board 3# name", "is_active": True},
    # Data without description, is_active
    {"name": "Board 4# name"},
    # Data with min length name
    {"name": "B", "description": "Board #3 description", "is_active": True},
    # Data with max length name(80)
    {
        "name": generate_str(80),
        "description": "Board #3 description",
        "is_active": True,
    },
    # Data with min length description
    {"name": "Board 5# name", "description": "", "is_active": True},
    # Data with max length description(255)
    {"name": "Board 5# name", "description": generate_str(255), "is_active": True},
]


@pytest.mark.parametrize("data", BOARDS_VALID_DATA)
def test_create_board_success(testapp, auth_user, data):
    url = url_for("api_v1.create_board")
    token = auth_user["auth_data"]["tokens"]["access"]["token"]
    headers = {"Authorization": f"Bearer {token}"}
    testapp.post_json(url, data, headers=headers, status=200)


BOARDS_INVALID_DATA = [
    # Data with zero length name
    {"name": "", "description": "Board #1 description", "is_active": True},
    # Data without name
    {"description": "Board #2 description", "is_active": True},
    # Data without None name
    {"name": None, "description": "Board #3 description", "is_active": True},
    # Data with exceeded length name
    {
        "name": generate_str(81),
        "description": "Board #1 description",
        "is_active": True,
    },
    # Data with exceeded description
    {"name": "Board 1# name", "description": generate_str(256), "is_active": True},
    # Data with None description
    {"name": "Board 2# name", "description": None, "is_active": True},
    # Data with incorrect name type
    {"name": True, "description": None, "is_active": True},
    # Data with incorrect description type
    {"name": "Board 3# name", "description": 12345, "is_active": True},
    # Data with incorrect is_active type
    {"name": "Board 4# name", "description": "Board #2 description", "is_active": 48},
]


@pytest.mark.parametrize("data", BOARDS_INVALID_DATA)
def test_create_board_failed(testapp, auth_user, data):
    url = url_for("api_v1.create_board")
    token = auth_user["auth_data"]["tokens"]["access"]["token"]
    headers = {"Authorization": f"Bearer {token}"}
    testapp.post_json(url, data, headers=headers, status=422)


def test_update_board(testapp, func_boards, auth_user):
    url = url_for(
        "api_v1.update_board", board_uuid=uuid.UUID(func_boards.get_single().uuid).hex
    )
    token = auth_user["auth_data"]["tokens"]["access"]["token"]

    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "name": "Board 1# updated name",
        "description": "Board #3 updated description",
        "is_active": True,
    }
    resp = testapp.put_json(url, data, headers=headers, status=200)

    assert resp.json["name"] == data["name"]
    assert resp.json["description"] == data["description"]
    assert resp.json["is_active"] == data["is_active"]


def test_update_board_not_exists(testapp, auth_user):
    url = url_for("api_v1.update_board", board_uuid=uuid.uuid4().hex)
    token = auth_user["auth_data"]["tokens"]["access"]["token"]

    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "name": "Board 1# updated name",
        "description": "Board #3 updated description",
        "is_active": True,
    }
    testapp.put_json(url, data, headers=headers, status=404)
