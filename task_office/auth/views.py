# -*- coding: utf-8 -*-
"""User views."""
from datetime import datetime

from flask import Blueprint
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import create_access_token, create_refresh_token

from .models import User
from .serializers import (
    user_schema,
    user_signup_schema,
    user_signin_schema,
    signed_schema,
)
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


@blueprint.route("/sign-in", methods=("post",))
@use_kwargs(user_signin_schema)
@marshal_with(signed_schema)
def sign_in(**kwargs):
    data = kwargs
    refresh_lf = datetime.timestamp(
        datetime.utcnow() + CONFIG.JWT_REFRESH_TOKEN_EXPIRES
    )
    access_lf = datetime.timestamp(datetime.utcnow() + CONFIG.JWT_ACCESS_TOKEN_EXPIRES)
    return {
        "user": data["user"],
        "tokens": {
            "access": {
                "lifetime": access_lf,
                "token": create_access_token(identity=data["user"], fresh=True),
            },
            "refresh": {
                "lifetime": refresh_lf,
                "token": create_refresh_token(identity=data["user"]),
            },
            "header_type": CONFIG.JWT_AUTH_HEADER_PREFIX,
            "time_zone_info": "utc",
        },
    }
