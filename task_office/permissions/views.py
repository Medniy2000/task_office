# -*- coding: utf-8 -*-
"""Permissions views."""

from flask import Blueprint
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import jwt_required

from .models import Permission
from .schemas.basic_schemas import (
    permission_in_schema,
    permission_out_schema,
    permissions_in_list_schema,
    permission_list_out_schema,
)
from ..core.helpers.listed_response import listed_response
from ..settings import CONFIG

blueprint = Blueprint(
    "permissions", __name__, url_prefix=CONFIG.API_V1_PREFIX + "/permissions"
)


@blueprint.route("/meta", methods=("get",))
@jwt_required
def get_meta_data():
    """
    Additional data for Permissions
    """
    data = dict()
    data["roles"] = Permission.Role.dict_choices()
    return data


@blueprint.route("", methods=("post",))
@jwt_required
@use_kwargs(permission_in_schema)
@marshal_with(permission_out_schema)
def create_permission(**kwargs):
    data = kwargs
    permission = Permission(**data)
    permission.save()
    return permission


@blueprint.route("", methods=("get",))
@jwt_required
@use_kwargs(permissions_in_list_schema)
def get_list_permission(**kwargs):
    data = kwargs
    query = Permission.query
    data = listed_response.serialize(
        query=query, query_params=data, schema=permission_list_out_schema
    )
    return data
