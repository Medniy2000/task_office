import uuid
from flask import url_for


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
        "api_v1.get_columns_meta_data",
        board_uuid=uuid.UUID(func_boards.get_single().uuid).hex,
    )
    token = auth_user["auth_data"]["tokens"]["access"]["token"]
    headers = {"Authorization": f"Bearer {token}"}
    testapp.get(url, headers=headers, status=200)


def test_get_board_columns_success(testapp, func_boards, auth_user):
    url = url_for(
        "api_v1.get_list_columns",
        board_uuid=uuid.UUID(func_boards.get_single().uuid).hex,
    )
    token = auth_user["auth_data"]["tokens"]["access"]["token"]
    headers = {"Authorization": f"Bearer {token}"}
    testapp.get(url, headers=headers, status=200)


def test_create_board_columns_success(
    testapp, auth_user, func_boards, columns_valid_data
):
    url = url_for(
        "api_v1.create_column", board_uuid=uuid.UUID(func_boards.get_single().uuid).hex,
    )
    token = auth_user["auth_data"]["tokens"]["access"]["token"]
    headers = {"Authorization": f"Bearer {token}"}
    testapp.post_json(url, columns_valid_data, headers=headers, status=200)


def test_create_board_columns_failed(
    testapp, auth_user, func_boards, columns_invalid_data
):
    url = url_for(
        "api_v1.create_column", board_uuid=uuid.UUID(func_boards.get_single().uuid).hex,
    )
    token = auth_user["auth_data"]["tokens"]["access"]["token"]
    headers = {"Authorization": f"Bearer {token}"}
    testapp.post_json(url, columns_invalid_data, headers=headers, status=422)


def test_update_board_columns(testapp, func_boards, auth_user):
    board_uuid = uuid.UUID(func_boards.get_single().uuid).hex
    column_uuid = uuid.UUID(func_boards.get_single().columns[0].uuid).hex
    url = url_for(
        "api_v1.update_column", board_uuid=board_uuid, column_uuid=column_uuid
    )
    token = auth_user["auth_data"]["tokens"]["access"]["token"]

    headers = {"Authorization": f"Bearer {token}"}
    data = {"name": "BoardColumn 1# name", "position": 1}
    resp = testapp.put_json(url, data, headers=headers, status=200)

    assert resp.json["name"] == data["name"]
    assert resp.json["position"] == data["position"]


def test_update_board_columns_not_exists(testapp, func_boards, auth_user):
    board_uuid = uuid.UUID(func_boards.get_single().uuid).hex
    column_uuid = uuid.uuid4().hex
    url = url_for(
        "api_v1.update_column", board_uuid=board_uuid, column_uuid=column_uuid
    )
    token = auth_user["auth_data"]["tokens"]["access"]["token"]

    headers = {"Authorization": f"Bearer {token}"}
    data = {"name": "BoardColumn 1# name", "position": 1}
    testapp.put_json(url, data, headers=headers, status=404)
