# -*- coding: utf-8 -*-
"""User views."""

from flask import Blueprint, request
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import (
    jwt_required,
    current_user,
)

from .serializers import user_schema
from ..settings import CONFIG

blueprint = Blueprint("user", __name__, url_prefix=CONFIG.API_V1_PREFIX)


@blueprint.route("/api/user", methods=("GET",))
@jwt_required
@marshal_with(user_schema)
def get_user():
    user = current_user
    # Not sure about this
    user.token = request.headers.environ["HTTP_AUTHORIZATION"].split("Token ")[1]
    return current_user


@blueprint.route("/api/user", methods=("PUT",))
@jwt_required
@use_kwargs(user_schema)
@marshal_with(user_schema)
def update_user(**kwargs):
    user = current_user
    # take in consideration the password
    password = kwargs.pop("password", None)
    if password:
        user.set_password(password)
    if "updated_at" in kwargs:
        kwargs["updated_at"] = user.created_at.replace(tzinfo=None)
    user.update(**kwargs)
    return user
