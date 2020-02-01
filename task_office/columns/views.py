# -*- coding: utf-8 -*-
"""Columns views."""

from flask import Blueprint
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import jwt_required

from task_office.boards.constants import BOARD_RETRIEVE_URL
from .schemas.basic_schemas import (
    column_in_schema,
    columns_in_list_schema,
    columns_list_out_schema,
    column_out_schema,
)
from ..core.helpers.listed_response import listed_response
from ..core.models.db_models import BoardColumn, Board
from ..core.utils import validate_request_url_uuid, query

blueprint = Blueprint("columns", __name__, url_prefix=BOARD_RETRIEVE_URL + "/columns")


@blueprint.route("/meta", methods=("get",))
@jwt_required
def get_meta_data(board_uuid):
    """
    Additional data for Columns
    """
    validate_request_url_uuid(Board, "uuid", board_uuid, True)
    data = dict()
    return data


@blueprint.route("", methods=("post",))
@jwt_required
@use_kwargs(column_in_schema)
@marshal_with(column_out_schema)
def create_column(board_uuid, **kwargs):
    data = kwargs
    validate_request_url_uuid(Board, "uuid", board_uuid, True)

    column = BoardColumn(board_uuid=board_uuid, **data)
    column.save()
    return column


@blueprint.route("", methods=("get",))
@jwt_required
@use_kwargs(columns_in_list_schema)
def get_list_columns(board_uuid, **kwargs):
    data = kwargs

    # Check board_uuid in request_url
    validate_request_url_uuid(Board, "uuid", board_uuid, True)

    columns = query(BoardColumn, board_uuid=str(board_uuid))

    # Serialize to paginated response
    data = listed_response.serialize(
        query=columns, query_params=data, schema=columns_list_out_schema
    )
    return data
