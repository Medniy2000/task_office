# -*- coding: utf-8 -*-
"""Permissions views."""
from flask import Blueprint, request
from flask_apispec import use_kwargs, marshal_with
from flask_babel import lazy_gettext as _
from flask_jwt_extended import jwt_required

from .models import Permission
from .schemas.basic_schemas import (
    permission_in_schema,
    permission_out_schema,
    permissions_in_list_schema,
    permission_list_out_schema,
)
from ..boards import BOARD_RETRIEVE_URL
from ..core.helpers.listed_response import listed_response
from ..core.utils import is_uuid
from ..exceptions import InvalidUsage

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

    perm = Permission.query.filter_by(board_uuid=board_uuid).first()
    if not perm:
        raise InvalidUsage(messages=[_("Not found")], status_code=404)

    data = dict()
    data["roles"] = Permission.Role.dict_choices()
    return data


@blueprint.route("", methods=("post",))
@jwt_required
@use_kwargs(permission_in_schema)
@marshal_with(permission_out_schema)
def create_permission(**kwargs):
    data = kwargs
    if data["board_uuid"] not in request.url:
        raise InvalidUsage(messages=[_("Not found")], status_code=404)
    permission = Permission(**data)
    permission.save()
    return permission


@blueprint.route("", methods=("get",))
@jwt_required
@use_kwargs(permissions_in_list_schema)
def get_list_permission(**kwargs):
    data = kwargs
    if str(data["board_uuid"]) not in request.url:
        raise InvalidUsage(messages=[_("Not found")], status_code=404)

    data = listed_response.serialize(
        query=Permission.query, query_params=data, schema=permission_list_out_schema
    )
    return data
