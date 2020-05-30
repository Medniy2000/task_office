import uuid

import pytest
from flask import url_for

from task_office.core.utils import generate_str


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


TASKS_VALID_DATA = [
    # Typical  task data
    {
        "label": "Label #1",
        "expire_at": "2020-05-25 05:30:11",
        "name": "Task #1 name",
        "description": "Task #1 description",
        "position": 1,
        "state": 1,
        "column_uuid": None,
        "performers": [],
    },
    # Task with max label name
    {
        "label": generate_str(size=80),
        "expire_at": "2020-05-25 05:30:11",
        "name": "Task #2 name",
        "description": "Task #2 description",
        "position": 1,
        "state": 1,
        "column_uuid": None,
        "performers": [],
    },
    # Task without label
    {
        "expire_at": "2020-05-25 05:30:11",
        "name": "Task #3 name",
        "description": "Task #3 description",
        "position": 1,
        "state": 1,
        "column_uuid": None,
        "performers": [],
    },
    # Task without expire_at
    {
        "label": "Label #1",
        "name": "Task #4 name",
        "description": "Task #4 description",
        "position": 1,
        "state": 1,
        "column_uuid": None,
        "performers": [],
    },
    # Task with min name length
    {
        "label": "Label #1",
        "expire_at": "2020-05-25 05:30:11",
        "name": "T",
        "description": "Task #5 description",
        "position": 1,
        "state": 1,
        "column_uuid": None,
        "performers": [],
    },
    # Task with max name length
    {
        "label": "Label #1",
        "expire_at": "2020-05-25 05:30:11",
        "name": "Task #6 name",
        "description": "Task #6 description",
        "position": 1,
        "state": 1,
        "column_uuid": None,
        "performers": [],
    },
    # Task with max description length
    {
        "label": "Label #1",
        "expire_at": "2020-05-25 05:30:11",
        "name": "Task #7 name",
        "description": generate_str(120),
        "position": 1,
        "state": 1,
        "column_uuid": None,
        "performers": [],
    },
    # Task without state
    {
        "label": "Label #1",
        "expire_at": "2020-05-25 05:30:11",
        "name": "Task #8 name",
        "description": "Task #8 description",
        "position": 1,
        "column_uuid": None,
        "performers": [],
    },
    # Task without position
    {
        "label": "Label #1",
        "expire_at": "2020-05-25 05:30:11",
        "name": "Task #9 name",
        "description": "Task #9 description",
        "state": 1,
        "column_uuid": None,
        "performers": [],
    },
]


@pytest.mark.parametrize("data", TASKS_VALID_DATA)
def create_tasks_success(testapp, func_boards, auth_user, data):
    url = url_for(
        "api_v1.create_task", board_uuid=uuid.UUID(func_boards.get_single().uuid).hex,
    )

    data["performers"].apend(auth_user["auth_data"]["uuid"])
    data["column_uuid"] = func_boards.get_single().columns[0].uuid

    token = auth_user["auth_data"]["tokens"]["access"]["token"]
    headers = {"Authorization": f"Bearer {token}"}

    testapp.post_json(url, data, headers=headers, status=200)


TASKS_INVALID_DATA = [
    # Task with None expire_at
    {
        "label": "Label #1",
        "expire_at": None,
        "name": "Task #1 name",
        "description": "Task #1 description",
        "position": 1,
        "state": 1,
        "column_uuid": None,
        "performers": [],
    },
    # Task with None label
    {
        "label": None,
        "expire_at": "2020-05-25 05:30:11",
        "name": "Task #1 name",
        "description": "Task #1 description",
        "position": 1,
        "state": 1,
        "column_uuid": None,
        "performers": [],
    },
    # Task with empty name
    {
        "label": "Label #1",
        "expire_at": "2020-05-25 05:30:11",
        "name": "",
        "description": "Task #1 description",
        "position": 1,
        "state": 1,
        "column_uuid": None,
        "performers": [],
    },
    # Task with exceeded name length
    {
        "label": "Label #1",
        "expire_at": "2020-05-25 05:30:11",
        "name": generate_str(120),
        "description": "Task #1 description",
        "position": 1,
        "state": 1,
        "column_uuid": None,
        "performers": [],
    },
    # Task with exceeded description length
    {
        "label": "Label #1",
        "expire_at": "2020-05-25 05:30:11",
        "name": "Task #1 name",
        "description": generate_str(121),
        "position": 1,
        "state": 1,
        "column_uuid": None,
        "performers": [],
    },
    # Task with None state
    {
        "label": "Label #1",
        "expire_at": "2020-05-25 05:30:11",
        "name": "Task #1 name",
        "description": "Task #1 description",
        "position": 1,
        "state": None,
        "column_uuid": None,
        "performers": [],
    },
    # Task with None position
    {
        "label": "Label #1",
        "expire_at": "2020-05-25 05:30:11",
        "name": "Task #1 name",
        "description": "Task #1 description",
        "position": None,
        "state": 1,
        "column_uuid": None,
        "performers": [],
    },
]


@pytest.mark.parametrize("data", TASKS_VALID_DATA)
def create_tasks_failed(testapp, func_boards, auth_user, data):
    url = url_for("api_v1.create_task", board_uuid=func_boards.get_single().uuid,)

    data["performers"].apend(auth_user["auth_data"]["uuid"])
    data["column_uuid"] = func_boards.get_single().columns[0].uuid

    token = auth_user["auth_data"]["tokens"]["access"]["token"]
    headers = {"Authorization": f"Bearer {token}"}

    testapp.post_json(url, data, headers=headers, status=422)


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
