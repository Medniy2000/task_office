import pytest

from task_office.core.utils import generate_str

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


@pytest.fixture(params=TASKS_VALID_DATA)
def tasks_valid_data(request):
    return request.param


@pytest.fixture(params=TASKS_INVALID_DATA)
def tasks_invalid_data(request):
    return request.param
