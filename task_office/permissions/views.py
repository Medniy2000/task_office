"""Permissions views."""
import uuid
from datetime import datetime

from flask import Blueprint
from flask_apispec import use_kwargs, marshal_with
from flask_babel import lazy_gettext as _
from flask_jwt_extended import jwt_required

from task_office.boards.constants import BOARD_RETRIEVE_URL
from .schemas.basic_schemas import (
    permission_query_schema,
    permission_dump_schema,
    permissions_list_query_schema,
    permission_list_dump_schema,
)
from ..auth.utils import permission, reset_permissions
from ..core.helpers.listed_response import listed_response
from ..core.models.db_models import Permission, Board
from ..core.utils import is_uuid, non_empty_query_required, empty_query_required
from ..exceptions import InvalidUsage

blueprint = Blueprint(
    "permissions", __name__, url_prefix=BOARD_RETRIEVE_URL + "/permissions"
)


@blueprint.route("/meta", methods=("get",))
@jwt_required
@permission(required_role=Permission.Role.EDITOR.value)
def get_meta_data(board_uuid):
    """
    Additional data for Permissions
    """
    if not is_uuid(board_uuid):
        raise InvalidUsage(messages=[_("Not found")], status_code=404)
    non_empty_query_required(Permission, board_uuid=str(board_uuid))

    data = dict()
    data["roles"] = Permission.Role.dict_choices()
    return data


@blueprint.route("", methods=("post",))
@jwt_required
@use_kwargs(permission_query_schema)
@marshal_with(permission_dump_schema)
@permission(required_role=Permission.Role.EDITOR.value)
def create_permission(board_uuid, **kwargs):
    """
    :param board_uuid:
    :param kwargs:
    :return:
    """
    data = kwargs
    # Check board_uuid in request_url
    if not is_uuid(board_uuid):
        raise InvalidUsage(messages=[_("Not found")], status_code=404)
    non_empty_query_required(Board, uuid=str(board_uuid))

    # Check board_uuid, user_uuid are unique for permission
    empty_query_required(Permission, board_uuid=board_uuid, user_uuid=data["user_uuid"])

    role = data["role"]
    if role == Permission.Role.OWNER.value:
        if Permission.query.filter_by(
            board_uuid=board_uuid, role=Permission.Role.OWNER.value
        ).first():
            raise InvalidUsage(messages=[_("Not allowed")], status_code=422)

    perm = Permission(board_uuid=board_uuid, **data)
    perm.save()
    reset_permissions(uuid.UUID(perm.user_uuid).hex)
    return permission


@blueprint.route("/<permission_uuid>", methods=("put",))
@jwt_required
@use_kwargs(permission_query_schema)
@marshal_with(permission_dump_schema)
@permission(required_role=Permission.Role.EDITOR.value)
def update_permission(board_uuid, permission_uuid, **kwargs):
    """
    :param board_uuid:
    :param permission_uuid:
    :param kwargs:
    :return:
    """
    data = kwargs
    # Check is valid board uuid and permission_uuid in request url
    if not is_uuid(board_uuid) or not is_uuid(permission_uuid):
        raise InvalidUsage(messages=[_("Not found")], status_code=404)

    role = data["role"]
    if role == Permission.Role.OWNER.value:
        if Permission.query.filter_by(
            board_uuid=board_uuid, role=Permission.Role.OWNER.value
        ).first():
            raise InvalidUsage(messages=[_("Not allowed")], status_code=422)

    perm = non_empty_query_required(
        Permission, uuid=str(permission_uuid), board_uuid=str(board_uuid)
    )[1]

    perm.update(updated_at=datetime.utcnow(), **data)
    perm.save()
    reset_permissions(uuid.UUID(perm.user_uuid).hex)
    return permission


@blueprint.route("", methods=("get",))
@jwt_required
@use_kwargs(permissions_list_query_schema)
@permission(required_role=Permission.Role.STAFF.value)
def get_list_permission(board_uuid, **kwargs):
    """
    :param board_uuid:
    :param kwargs:
    :return:
    """
    data = kwargs
    # Check board_uuid in request_url
    if not is_uuid(board_uuid):
        raise InvalidUsage(messages=[_("Not found")], status_code=404)

    perms = non_empty_query_required(Permission, board_uuid=str(board_uuid))[0]

    # Serialize to paginated response
    data = listed_response.serialize(
        query=perms, query_params=data, schema=permission_list_dump_schema
    )
    return data


@blueprint.route("/<permission_uuid>", methods=("get",))
@jwt_required
@marshal_with(permission_dump_schema)
@permission(required_role=Permission.Role.STAFF.value)
def get_permission_by_uuid(board_uuid, permission_uuid):
    """
    :param board_uuid:
    :param permission_uuid:
    :return:
    """
    # Check is valid board uuid and permission_uuid in request url
    if not is_uuid(board_uuid) or not is_uuid(permission_uuid):
        raise InvalidUsage(messages=[_("Not found")], status_code=404)

    perm = non_empty_query_required(
        Permission, uuid=str(permission_uuid), board_uuid=str(board_uuid)
    )
    perm = perm[1]

    return perm
