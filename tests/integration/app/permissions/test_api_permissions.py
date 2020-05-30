import uuid

import pytest
from flask import url_for

from task_office.core.models.db_models import Permission
from tests.factories import UserFactory


def test_get_board_permissions_list_without_auth(testapp, func_boards):
    url = url_for(
        "api_v1.get_list_permission",
        board_uuid=uuid.UUID(func_boards.get_single().uuid).hex,
    )
    testapp.get(url, status=401)


def test_create_board_permissions_without_auth(testapp, func_boards, func_users):
    board = func_boards.get_single()
    url = url_for("api_v1.create_permission", board_uuid=board.uuid)
    data = {"role": 2, "user_uuid": func_users.get_single().uuid}
    testapp.post_json(url, data, status=401)


def test_update_board_permission_without_auth(testapp, func_boards):
    board = func_boards.get_single()
    permission = board.perms[0]
    url = url_for(
        "api_v1.update_permission",
        board_uuid=board.uuid,
        permission_uuid=permission.uuid,
    )
    data = {
        "role": 3,
    }
    testapp.put_json(url, data, status=401)


def test_get_board_permission_without_auth(testapp, func_boards):
    board = func_boards.get_single()
    permission = board.perms[0]
    url = url_for(
        "api_v1.get_permission_by_uuid",
        board_uuid=board.uuid,
        permission_uuid=permission.uuid,
    )
    testapp.get(url, status=401)


def test_get_board_permissions_meta_without_auth(testapp, func_boards):
    board = func_boards.get_single()
    url = url_for("api_v1.get_permissions_meta_data", board_uuid=board.uuid,)
    testapp.get(url, status=401)


def test_get_board_permissions_list(testapp, func_boards):
    url = url_for(
        "api_v1.get_list_permission",
        board_uuid=uuid.UUID(func_boards.get_single().uuid).hex,
    )
    testapp.get(url, status=401)


def test_get_board_permission(testapp, func_boards, auth_user):
    board = func_boards.get_single()
    permission = board.perms[0]
    url = url_for(
        "api_v1.get_permission_by_uuid",
        board_uuid=board.uuid,
        permission_uuid=permission.uuid,
    )
    token = auth_user["auth_data"]["tokens"]["access"]["token"]
    headers = {"Authorization": f"Bearer {token}"}

    testapp.get(url, headers=headers, status=200)


def test_get_board_permissions_meta(testapp, func_boards, auth_user):
    board = func_boards.get_single()
    url = url_for("api_v1.get_permissions_meta_data", board_uuid=board.uuid,)

    token = auth_user["auth_data"]["tokens"]["access"]["token"]
    headers = {"Authorization": f"Bearer {token}"}

    testapp.get(url, headers=headers, status=200)


PERMISSIONS_VALID_DATA = [{"role": role} for role in Permission.Role.get_values()]


@pytest.mark.parametrize("data", PERMISSIONS_VALID_DATA)
def test_create_board_permissions(testapp, func_boards, auth_user, data):
    board = func_boards.get_single()
    url = url_for("api_v1.create_permission", board_uuid=board.uuid)
    data["user_uuid"] = UserFactory().uuid

    token = auth_user["auth_data"]["tokens"]["access"]["token"]
    headers = {"Authorization": f"Bearer {token}"}

    testapp.post_json(url, data, headers=headers, status=200)


def test_update_board_permission(testapp, auth_user, func_boards):
    permission = auth_user["current_user"].perms[0]

    url = url_for(
        "api_v1.update_permission",
        board_uuid=permission.board_uuid,
        permission_uuid=permission.uuid,
    )

    token = auth_user["auth_data"]["tokens"]["access"]["token"]
    headers = {"Authorization": f"Bearer {token}"}

    data = {
        "role": Permission.Role.STAFF.value,
        "user_uuid": auth_user["current_user"].uuid,
    }
    resp = testapp.put_json(url, data, headers=headers, status=200)

    assert resp.json["role"] == permission.role
