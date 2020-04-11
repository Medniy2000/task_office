"""User views."""
from datetime import datetime

from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
)

from .schemas import (
    user_schema,
    user_signup_schema,
    user_signin_schema,
    signed_schema,
    refreshed_access_tokens_schema,
)
from ..api.v1.views import bp
from ..core.models.db_models import User
from ..settings import app_config

APP_PREFIX = "/auth"


@bp.route(APP_PREFIX + "/sign-up", methods=("post",))
@use_kwargs(user_signup_schema)
@marshal_with(user_schema)
def sign_up(**kwargs):
    """
    :param kwargs:
    :return:
    """
    data = kwargs
    data.pop("password_confirm")
    user = User(**data)
    user.save()
    return user


@bp.route(APP_PREFIX + "/sign-in", methods=("post",))
@use_kwargs(user_signin_schema)
@marshal_with(signed_schema)
def sign_in(**kwargs):
    """
    :param kwargs:
    :return:
    """
    data = kwargs
    refresh_lf = datetime.timestamp(
        datetime.utcnow() + app_config.JWT_REFRESH_TOKEN_EXPIRES
    )
    access_lf = datetime.timestamp(
        datetime.utcnow() + app_config.JWT_ACCESS_TOKEN_EXPIRES
    )
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
            "header_type": app_config.JWT_AUTH_HEADER_PREFIX,
            "time_zone_info": app_config.TIME_ZONE,
        },
    }


@bp.route(APP_PREFIX + "/refresh", methods=("post",))
@jwt_refresh_token_required
@marshal_with(refreshed_access_tokens_schema)
def refresh(**kwargs):
    """
    :param kwargs:
    :return:
    """
    current_user = User.get_by_id(get_jwt_identity())
    access_lf = datetime.timestamp(
        datetime.utcnow() + app_config.JWT_ACCESS_TOKEN_EXPIRES
    )
    return {
        "access": {
            "lifetime": access_lf,
            "token": create_access_token(identity=current_user, fresh=True),
        },
        "time_zone_info": app_config.TIME_ZONE,
    }
