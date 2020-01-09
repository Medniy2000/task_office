# -*- coding: utf-8 -*-
"""User views."""
from datetime import datetime

from flask import Blueprint
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
)

from .models import User
from .schemas import (
    user_schema,
    user_signup_schema,
    user_signin_schema,
    signed_schema,
    refreshed_access_tokens_schema,
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
            "time_zone_info": CONFIG.TIME_ZONE,
        },
    }


@blueprint.route("/refresh", methods=("post",))
@jwt_refresh_token_required
@marshal_with(refreshed_access_tokens_schema)
def refresh(**kwargs):
    current_user = User.get_by_id(get_jwt_identity())
    access_lf = datetime.timestamp(datetime.utcnow() + CONFIG.JWT_ACCESS_TOKEN_EXPIRES)
    return {
        "access": {
            "lifetime": access_lf,
            "token": create_access_token(identity=current_user, fresh=True),
        },
        "time_zone_info": CONFIG.TIME_ZONE,
    }
