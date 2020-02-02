# -*- coding: utf-8 -*-
"""Columns views."""
from datetime import datetime

from flask import Blueprint
from flask_apispec import use_kwargs, marshal_with
from flask_babel import lazy_gettext as _
from flask_jwt_extended import jwt_required
from sqlalchemy import func

from task_office.boards.constants import BOARD_RETRIEVE_URL
from .schemas.basic_schemas import (
    column_post_schema,
    columns_in_list_schema,
    columns_list_out_schema,
    column_out_schema,
    column_put_schema,
)
from .utils import reset_columns_ordering
from ..core.helpers.listed_response import listed_response
from ..core.models.db_models import BoardColumn, Board
from ..core.utils import validate_request_url_uuid, non_empty_query_required
from ..exceptions import InvalidUsage
from ..extensions import db

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
@use_kwargs(column_post_schema)
@marshal_with(column_out_schema)
def create_column(board_uuid, **kwargs):
    data = kwargs
    validate_request_url_uuid(Board, "uuid", board_uuid, True)

    # validate max position
    data["position"] = data.get("position", 1)
    position = data["position"]
    if position > 1:
        max_position = db.session.query(func.max(BoardColumn.position)).scalar()
        max_position = 1 if max_position is None else max_position + 1
        if position > max_position:
            raise InvalidUsage(
                messages=[_("Must be between {} and {}".format(1, max_position))],
                status_code=422,
                key="position",
            )

    # validate unique name for board
    q_by_name = BoardColumn.query.filter_by(
        board_uuid=board_uuid, name=data["name"]
    ).first()
    if q_by_name:
        raise InvalidUsage(
            messages=[_("Already exists with value {}".format(data["name"]))],
            status_code=422,
            key="name",
        )

    column = BoardColumn(board_uuid=board_uuid, **data)
    column.save()

    reset_columns_ordering(column, board_uuid, position)

    return column


@blueprint.route("/<column_uuid>", methods=("put",))
@jwt_required
@use_kwargs(column_put_schema)
@marshal_with(column_out_schema)
def update_column(board_uuid, column_uuid, **kwargs):
    data = kwargs

    validate_request_url_uuid(Board, "uuid", board_uuid, True)
    validate_request_url_uuid(BoardColumn, "uuid", column_uuid, True)

    # validate max position value
    position = data.get("position", None)
    if position is not None and position > 1:
        max_position = db.session.query(func.max(BoardColumn.position)).scalar()
        max_position = 1 if max_position is None else max_position + 1

        if position > max_position:
            raise InvalidUsage(
                messages=[_("Must be between {} and {}.".format(1, max_position))],
                status_code=422,
                key="position",
            )

    # validate unique name for board
    q_by_name = BoardColumn.query.filter(
        BoardColumn.uuid != column_uuid,
        BoardColumn.board_uuid == board_uuid,
        BoardColumn.name == data["name"],
    ).first()
    if q_by_name:
        raise InvalidUsage(
            messages=[_("Already exists with value {}".format(data["name"]))],
            status_code=422,
            key="name",
        )

    column = non_empty_query_required(
        BoardColumn, uuid=str(column_uuid), board_uuid=str(board_uuid)
    )[1]

    if data:
        old_position = column.position
        column.update(updated_at=datetime.utcnow(), **data)
        column.save()
        if position:
            reset_columns_ordering(column, board_uuid, position, old_position)

    return column


@blueprint.route("", methods=("get",))
@jwt_required
@use_kwargs(columns_in_list_schema)
def get_list_columns(board_uuid, **kwargs):
    data = kwargs

    # Check board_uuid in request_url
    validate_request_url_uuid(Board, "uuid", board_uuid, True)

    columns = BoardColumn.query.order_by("position", "-id").filter_by(
        board_uuid=board_uuid
    )

    # Serialize to paginated response
    data = listed_response.serialize(
        query=columns, query_params=data, schema=columns_list_out_schema
    )
    return data
