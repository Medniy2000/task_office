import uuid

import pytest
from flask import request, url_for

from task_office.core.models.db_models import Board
from task_office.core.utils import (
    is_uuid,
    non_empty_query_required,
    empty_query_required,
    validate_request_url_uuid,
)
from task_office.exceptions import InvalidUsage


def test_is_uuid_success(valid_uuid_list):
    assert is_uuid(valid_uuid_list) is True


def test_is_uuid_failed(invalid_uuid_list):
    assert is_uuid(invalid_uuid_list) is False


def test_non_empty_query_required_success(func_boards):
    non_empty_query_required(Board, name=func_boards.get_single().name)


def test_non_empty_query_required_failed(invalid_boards_query_list):
    with pytest.raises(InvalidUsage):
        non_empty_query_required(Board, **invalid_boards_query_list)


def test_empty_query_required_success(invalid_boards_query_list):
    empty_query_required(Board, **invalid_boards_query_list)


def test_empty_query_required_failed(func_boards):
    with pytest.raises(InvalidUsage):
        empty_query_required(Board, name=func_boards.get_single().name)


def test_request_url_uuid_success(
    func_boards, testapp,
):
    for item in func_boards.get_list():
        uuid_hexed = uuid.UUID(str(item.uuid)).hex
        request.url = url_for("api_v1.get_board", board_uuid=uuid_hexed,)
        validate_request_url_uuid(Board, "uuid", uuid_hexed, True)


def test_request_url_uuid_failed_case1(invalid_uuid_list, testapp):
    with pytest.raises(InvalidUsage):
        uuid_hexed = invalid_uuid_list
        url = f"http://some-host/api/v1/boards/{uuid_hexed}/"
        request.url = url
        validate_request_url_uuid(Board, "uuid", uuid_hexed, False)


def test_request_url_uuid_failed_case2(testapp):
    for item in range(2):
        with pytest.raises(InvalidUsage):
            uuid_hexed = uuid.uuid4().hex
            request.url = url_for("api_v1.get_board", board_uuid=uuid_hexed,)
            validate_request_url_uuid(Board, "uuid", uuid_hexed, True)
