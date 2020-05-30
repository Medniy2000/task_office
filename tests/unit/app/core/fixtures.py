import pytest

VALID_UUID_LIST = [
    "31b2e088-d37b-4e90-9983-1ef6f44b932a",
    "31b2e088d37b4e9099831ef6f44b932a",
]

INVALID_UUID_LIST = [
    "31b2e088-d37b-4e90-9983-1ef6f44b932z",
    "12345678910",
    "ZXsdpk12-21-zxczxcl-58484848-zx-xcxc",
]

INVALID_BOARDS_QUERY_DATA = [{"uuid": item} for item in VALID_UUID_LIST]


@pytest.fixture(params=VALID_UUID_LIST)
def valid_uuid_list(request):
    return request.param


@pytest.fixture(params=INVALID_UUID_LIST)
def invalid_uuid_list(request):
    return request.param


@pytest.fixture(params=INVALID_BOARDS_QUERY_DATA)
def invalid_boards_query_list(request, db):
    return request.param
