import pytest

from task_office.core.utils import generate_str

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


@pytest.fixture(params=BOARDS_VALID_DATA)
def boards_valid_data(request):
    return request.param


@pytest.fixture(params=BOARDS_INVALID_DATA)
def boards_invalid_data(request):
    return request.param
