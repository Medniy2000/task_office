# -*- coding: utf-8 -*-
"""Boards views."""
from flask_babel import lazy_gettext as _
from flask import Blueprint
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import jwt_required, get_current_user

from .constants import BOARDS_PREFIX
from .schemas.basic_schemas import (
    board_in_schema,
    boards_in_list_schema,
    boards_list_out_schema,
    board_out_schema,
)
from ..core.helpers.listed_response import listed_response
from ..core.models.db_models import Board, Permission
from ..core.utils import is_uuid
from ..exceptions import InvalidUsage
from ..utils import empty_query_required, non_empty_query_required

blueprint = Blueprint("boards", __name__, url_prefix=BOARDS_PREFIX)


@blueprint.route("", methods=("post",))
@jwt_required
@use_kwargs(board_in_schema)
@marshal_with(board_out_schema)
def create_boards(**kwargs):
    data = kwargs
    # Check name, owner_uuid are unique for board
    empty_query_required(Board, name=data["name"], owner_uuid=str(data["owner_uuid"]))
    board = Board(**data)
    board.save()

    # Create permission for creator
    Permission(
        user_uuid=str(data["owner_uuid"]),
        board_uuid=str(board.uuid),
        role=Permission.Role.OWNER.value,
    ).save()

    return board


@blueprint.route("", methods=("get",))
@jwt_required
@use_kwargs(boards_in_list_schema)
def get_list_boards(**kwargs):
    data = kwargs
    user = get_current_user()

    boards = Board.query.join(Permission).filter(Permission.user_uuid == user.uuid)
    # Serialize to paginated response
    data = listed_response.serialize(
        query=boards, query_params=data, schema=boards_list_out_schema
    )
    return data


@blueprint.route("/<board_uuid>", methods=("get",))
@jwt_required
@marshal_with(board_out_schema)
def get_board_by_uuid(board_uuid):
    # board_uuid in request url
    if not is_uuid(board_uuid):
        raise InvalidUsage(messages=[_("Not found")], status_code=404)

    board = non_empty_query_required(Board, uuid=str(board_uuid))[1]

    return board