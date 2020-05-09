import uuid
from flask import url_for


def test_get_tasks_without_auth(testapp, func_boards):
    board_uuid = func_boards.get_single().uuid
    url = url_for("api_v1.get_list_tasks", board_uuid=board_uuid,)
    testapp.get(url, status=401)


def test_get_tasks_by_columns_without_auth(testapp, func_boards):
    board_uuid = func_boards.get_single().uuid
    url = url_for("api_v1.get_list_tasks_by_columns", board_uuid=board_uuid,)
    testapp.get(url, status=401)


def test_create_task_without_auth(testapp, func_boards):
    url = url_for(
        "api_v1.create_task", board_uuid=uuid.UUID(func_boards.get_single().uuid).hex,
    )
    data = {
        "label": "Label#",
        "expire_at": "2020-05-25 05:30:11",
        "name": "Task # name",
        "description": "Task # description",
        "position": 1,
        "state": 1,
        "column_uuid": func_boards.get_single().columns[0].uuid,
    }
    testapp.post_json(url, data, status=401)


def test_update_task_without_auth(testapp, func_boards):
    task_uuid = func_boards.get_single().columns[0].tasks[0].uuid
    board_uuid = func_boards.get_single().uuid
    url = url_for("api_v1.update_task", board_uuid=board_uuid, task_uuid=task_uuid)
    data = {
        "label": "Label#",
        "expire_at": "2020-05-25 05:30:11",
        "name": "Task # name",
        "description": "Task # description",
        "position": 1,
        "state": 1,
        "column_uuid": func_boards.get_single().columns[0].uuid,
    }
    testapp.put_json(url, data, status=401)


def test_get_tasks_metadata_without_auth(testapp, func_boards):
    url = url_for(
        "api_v1.get_tasks_meta_data",
        board_uuid=uuid.UUID(func_boards.get_single().uuid).hex,
    )
    testapp.get(url, status=401)


def test_get_tasks_metadata_success(testapp, func_boards, auth_user):
    url = url_for(
        "api_v1.get_tasks_meta_data",
        board_uuid=uuid.UUID(func_boards.get_single().uuid).hex,
    )
    token = auth_user["auth_data"]["tokens"]["access"]["token"]
    headers = {"Authorization": f"Bearer {token}"}
    testapp.get(url, headers=headers, status=200)


def test_get_tasks(testapp, func_boards, auth_user):
    board_uuid = func_boards.get_single().uuid
    url = url_for("api_v1.get_list_tasks", board_uuid=board_uuid,)
    token = auth_user["auth_data"]["tokens"]["access"]["token"]
    headers = {"Authorization": f"Bearer {token}"}
    testapp.get(url, headers=headers, status=200)


def test_get_tasks_by_columns(testapp, func_boards, auth_user):
    board_uuid = func_boards.get_single().uuid
    url = url_for("api_v1.get_list_tasks_by_columns", board_uuid=board_uuid,)
    token = auth_user["auth_data"]["tokens"]["access"]["token"]
    headers = {"Authorization": f"Bearer {token}"}
    testapp.get(url, headers=headers, status=200)


def create_tasks_success(testapp, func_boards, auth_user, tasks_valid_data):
    url = url_for(
        "api_v1.create_task", board_uuid=uuid.UUID(func_boards.get_single().uuid).hex,
    )

    tasks_valid_data["performers"].apend(auth_user["auth_data"]["uuid"])
    tasks_valid_data["column_uuid"] = func_boards.get_single().columns[0].uuid

    token = auth_user["auth_data"]["tokens"]["access"]["token"]
    headers = {"Authorization": f"Bearer {token}"}

    testapp.post_json(url, tasks_valid_data, headers=headers, status=200)


def create_tasks_failed(testapp, func_boards, auth_user, tasks_invalid_data):
    url = url_for("api_v1.create_task", board_uuid=func_boards.get_single().uuid,)

    tasks_invalid_data["performers"].apend(auth_user["auth_data"]["uuid"])
    tasks_invalid_data["column_uuid"] = func_boards.get_single().columns[0].uuid

    token = auth_user["auth_data"]["tokens"]["access"]["token"]
    headers = {"Authorization": f"Bearer {token}"}

    testapp.post_json(url, tasks_invalid_data, headers=headers, status=422)


def update_tasks_success(testapp, func_boards, auth_user):
    board = func_boards.get_single()

    token = auth_user["auth_data"]["tokens"]["access"]["token"]
    headers = {"Authorization": f"Bearer {token}"}

    item_number = 100
    for task in board.columns[0].tasks:
        url = url_for("api_v1.update_task", board_uuid=board.uuid, task_uuid=task.uuid)
        data = (
            {
                "label": f"Label #{item_number}",
                "expire_at": "2020-05-25 05:30:11",
                "name": f"Task #{item_number} name",
                "description": f"Task #{item_number} description",
            },
        )
        resp = testapp.put_json(url, data, headers=headers, status=200)
        resp_data = resp.json
        assert data["label"] == resp_data["label"]
        assert data["name"] == resp_data["name"]
        assert data["description"] == resp_data["description"]
