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


def test_create_board_success(testapp, auth_user, boards_valid_data):
    url = url_for("api_v1.create_board")
    token = auth_user["auth_data"]["tokens"]["access"]["token"]
    headers = {"Authorization": f"Bearer {token}"}
    testapp.post_json(url, boards_valid_data, headers=headers, status=200)


def test_create_board_failed(testapp, auth_user, boards_invalid_data):
    url = url_for("api_v1.create_board")
    token = auth_user["auth_data"]["tokens"]["access"]["token"]
    headers = {"Authorization": f"Bearer {token}"}
    testapp.post_json(url, boards_invalid_data, headers=headers, status=422)


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
