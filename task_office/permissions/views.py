# -*- coding: utf-8 -*-
"""Permissions views."""

from flask import Blueprint
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import jwt_required

from .models import Permission
from .serializers import permission_in_schema, permission_out_schema
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


@blueprint.route("/", methods=("post",))
@jwt_required
@use_kwargs(permission_in_schema)
@marshal_with(permission_out_schema)
def create_permission(**kwargs):
    data = kwargs
    permission = Permission(**data)
    permission.save()
    return permission
