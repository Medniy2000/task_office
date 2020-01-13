# -*- coding: utf-8 -*-
"""Permissions views."""
from datetime import datetime

from flask import Blueprint
from flask_apispec import use_kwargs, marshal_with
from flask_babel import lazy_gettext as _
from flask_jwt_extended import jwt_required

from task_office.boards.constants import BOARD_RETRIEVE_URL
from .schemas.basic_schemas import (
    permission_in_schema,
    permission_out_schema,
    permissions_in_list_schema,
    permission_list_out_schema,
)
from ..core.helpers.listed_response import listed_response
from ..core.models.db_models import Permission, Board
from ..core.utils import is_uuid
from ..exceptions import InvalidUsage
from ..utils import non_empty_query_required, empty_query_required

blueprint = Blueprint(
    "permissions", __name__, url_prefix=BOARD_RETRIEVE_URL + "/permissions"
)


@blueprint.route("/meta", methods=("get",))
@jwt_required
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
@use_kwargs(permission_in_schema)
@marshal_with(permission_out_schema)
def create_permission(board_uuid, **kwargs):
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

    permission = Permission(board_uuid=board_uuid, **data)
    permission.save()
    return permission


@blueprint.route("/<permission_uuid>", methods=("put",))
@jwt_required
@use_kwargs(permission_in_schema)
@marshal_with(permission_out_schema)
def update_permission(board_uuid, permission_uuid, **kwargs):
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

    permission = non_empty_query_required(
        Permission, uuid=str(permission_uuid), board_uuid=str(board_uuid)
    )[1]

    permission.update(updated_at=datetime.utcnow(), **data)
    permission.save()
    return permission


@blueprint.route("", methods=("get",))
@jwt_required
@use_kwargs(permissions_in_list_schema)
def get_list_permission(board_uuid, **kwargs):
    data = kwargs
    # Check board_uuid in request_url
    if not is_uuid(board_uuid):
        raise InvalidUsage(messages=[_("Not found")], status_code=404)

    permissions = non_empty_query_required(Permission, board_uuid=str(board_uuid))[0]

    # Serialize to paginated response
    data = listed_response.serialize(
        query=permissions, query_params=data, schema=permission_list_out_schema
    )
    return data


@blueprint.route("/<permission_uuid>", methods=("get",))
@jwt_required
@marshal_with(permission_out_schema)
def get_permission_by_uuid(board_uuid, permission_uuid):
    # Check is valid board uuid and permission_uuid in request url
    if not is_uuid(board_uuid) or not is_uuid(permission_uuid):
        raise InvalidUsage(messages=[_("Not found")], status_code=404)

    permission = non_empty_query_required(
        Permission, uuid=str(permission_uuid), board_uuid=str(board_uuid)
    )
    permission = permission.first()

    return permission
