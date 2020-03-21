"""Boards views."""
from flask import Blueprint
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import jwt_required, get_current_user
from sqlalchemy.orm import aliased

from .constants import BOARDS_PREFIX
from .schemas.basic_schemas import (
    board_put_schema,
    board_list_query_schema,
    board_list_dump_schema,
    board_dump_schema,
    user_list_by_board_query_schema,
)
from ..auth.utils import permission
from ..core.helpers.listed_response import listed_response
from ..core.models.db_models import Board, Permission, User
from ..core.schemas.nested_schemas import nested_user_list_dump_schema
from ..core.utils import empty_query_required, validate_request_url_uuid

blueprint = Blueprint("boards", __name__, url_prefix=BOARDS_PREFIX)


@blueprint.route("", methods=("post",))
@jwt_required
@use_kwargs(board_put_schema)
@marshal_with(board_dump_schema)
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
@use_kwargs(board_list_query_schema)
def get_list_boards(**kwargs):
    data = kwargs
    user = get_current_user()

    boards = Board.query.join(Permission).filter(Permission.user_uuid == user.uuid)
    # Serialize to paginated response
    data = listed_response.serialize(
        query=boards, query_params=data, schema=board_list_dump_schema
    )
    return data


@blueprint.route("/<board_uuid>", methods=("get",))
@jwt_required
@marshal_with(board_dump_schema)
@permission(required_role=Permission.Role.STAFF.value)
def get_board(board_uuid):

    board = validate_request_url_uuid(Board, "uuid", board_uuid, True)[1]

    return board


@blueprint.route("/<board_uuid>/users", methods=("get",))
@jwt_required
@use_kwargs(user_list_by_board_query_schema)
@permission(required_role=Permission.Role.STAFF.value)
def get_board_users(board_uuid, **kwargs):
    data = kwargs

    # board_uuid in request url
    validate_request_url_uuid(Board, "uuid", board_uuid, True)

    perms_q = aliased(
        Permission.query.filter(Permission.board_uuid == board_uuid).subquery(),
        name="perms",
    )
    users_q = User.query.join(perms_q).filter()
    data = listed_response.serialize(
        query=users_q, query_params=data, schema=nested_user_list_dump_schema
    )
    return data
