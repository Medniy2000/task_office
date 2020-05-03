import pytest

from task_office.core.utils import generate_str

COLUMNS_VALID_DATA = [
    # Typical  board data
    {"name": "BoardColumn 1# name", "position": 1},
    # With min length name
    {"name": "B", "position": 1},
    # With max length name
    {"name": generate_str(120), "position": 1},
]

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


@pytest.fixture(params=COLUMNS_VALID_DATA)
def columns_valid_data(request):
    return request.param


@pytest.fixture(params=COLUMNS_INVALID_DATA)
def columns_invalid_data(request):
    return request.param
