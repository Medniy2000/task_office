import uuid

import pytest
from flask import url_for

from task_office.core.utils import generate_str


def test_get_board_columns_without_auth(testapp, func_boards):
    url = url_for(
        "api_v1.get_list_columns",
        board_uuid=uuid.UUID(func_boards.get_single().uuid).hex,
    )
    testapp.get(url, status=401)


def test_create_board_columns_without_auth(testapp, func_boards):
    url = url_for(
        "api_v1.create_column", board_uuid=uuid.UUID(func_boards.get_single().uuid).hex,
    )
    data = {
        "name": "Column # name",
        "position": 1,
    }
    testapp.post_json(url, data, status=401)


def test_get_board_columns_metadata_without_auth(testapp, func_boards):
    url = url_for(
        "api_v1.get_columns_meta_data",
        board_uuid=uuid.UUID(func_boards.get_single().uuid).hex,
    )
    testapp.get(url, status=401)


def test_get_board_columns_metadata_success(testapp, func_boards, auth_user):
    url = url_for(
        "api_v1.get_columns_meta_data", board_uuid=func_boards.get_single().uuid,
    )
    token = auth_user["auth_data"]["tokens"]["access"]["token"]
    headers = {"Authorization": f"Bearer {token}"}
    testapp.get(url, headers=headers, status=200)


def test_get_board_columns_success(testapp, func_boards, auth_user):
    url = url_for("api_v1.get_list_columns", board_uuid=func_boards.get_single().uuid,)
    token = auth_user["auth_data"]["tokens"]["access"]["token"]
    headers = {"Authorization": f"Bearer {token}"}
    testapp.get(url, headers=headers, status=200)


COLUMNS_VALID_DATA = [
    # Typical  board data
    {"name": "BoardColumn 1# name", "position": 1},
    # With min length name
    {"name": "B", "position": 1},
    # With max length name
    {"name": generate_str(120), "position": 1},
]


@pytest.mark.parametrize("data", COLUMNS_VALID_DATA)
def test_create_board_columns_success(testapp, auth_user, func_boards, data):
    url = url_for("api_v1.create_column", board_uuid=func_boards.get_single().uuid,)
    token = auth_user["auth_data"]["tokens"]["access"]["token"]
    headers = {"Authorization": f"Bearer {token}"}
    testapp.post_json(url, data, headers=headers, status=200)


COLUMNS_INVALID_DATA = [
    # With empty name
    {"name": "", "position": 1},
    # With None Name
    {"name": None, "position": 1},
    # Without name
    {"position": 1},
    # With exceeded name length
    {"name": generate_str(121), "position": 1},
    #  With to small position
    {"name": "BoardColumn 1# name", "position": 0},
    #  With None position
    {"name": "BoardColumn 1# name", "position": None},
    #  Without position
    {"name": "BoardColumn 1# name"},
]


@pytest.mark.parametrize("data", COLUMNS_INVALID_DATA)
def test_create_board_columns_failed(testapp, auth_user, func_boards, data):
    url = url_for("api_v1.create_column", board_uuid=func_boards.get_single().uuid,)
    token = auth_user["auth_data"]["tokens"]["access"]["token"]
    headers = {"Authorization": f"Bearer {token}"}
    testapp.post_json(url, data, headers=headers, status=422)


def test_update_board_columns(testapp, func_boards, auth_user):
    board = func_boards.get_single()
    column = board.columns[0]
    url = url_for(
        "api_v1.update_column", board_uuid=board.uuid, column_uuid=column.uuid
    )
    token = auth_user["auth_data"]["tokens"]["access"]["token"]

    headers = {"Authorization": f"Bearer {token}"}
    data = {"name": "BoardColumn 1# name", "position": 1}
    resp = testapp.put_json(url, data, headers=headers, status=200)

    assert resp.json["name"] == data["name"]
    assert resp.json["position"] == data["position"]


def test_update_board_columns_not_exists(testapp, func_boards, auth_user):
    board_uuid = func_boards.get_single()
    column_uuid = uuid.uuid4().hex
    url = url_for(
        "api_v1.update_column", board_uuid=board_uuid, column_uuid=column_uuid
    )
    token = auth_user["auth_data"]["tokens"]["access"]["token"]

    headers = {"Authorization": f"Bearer {token}"}
    data = {"name": "BoardColumn 1# name", "position": 1}
    testapp.put_json(url, data, headers=headers, status=404)
