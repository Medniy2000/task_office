# -*- coding: utf-8 -*-
"""User views."""

from flask import Blueprint
from flask_apispec import use_kwargs, marshal_with

from .models import User
from .serializers import user_schema, user_signup_schema
from ..settings import CONFIG

blueprint = Blueprint("auth", __name__, url_prefix=CONFIG.API_V1_PREFIX + "/auth")


@blueprint.route("/sign-up", methods=("post",))
@use_kwargs(user_signup_schema)
@marshal_with(user_schema)
def sign_up(**kwargs):
    data = kwargs
    data.pop("password_confirm")
    user = User(**data)
    user.save()
    return user
