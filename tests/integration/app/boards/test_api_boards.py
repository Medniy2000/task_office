import uuid

from flask import url_for


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
