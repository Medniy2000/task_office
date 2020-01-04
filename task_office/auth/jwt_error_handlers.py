from flask_babel import lazy_gettext as _
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended.exceptions import (
    NoAuthorizationError,
    CSRFError,
    InvalidHeaderError,
    JWTDecodeError,
    WrongTokenError,
    RevokedTokenError,
    FreshTokenRequired,
    UserLoadError,
    UserClaimsVerificationError,
)
from jwt import ExpiredSignatureError, InvalidTokenError

from task_office.exceptions import InvalidUsage


def handle_auth_error(e):
    return InvalidUsage(messages=[str(e)], status_code=401)


def handle_expired_error(e):
    return InvalidUsage(messages=[str(e)], status_code=401)


def handle_invalid_header_error(e):
    return InvalidUsage(messages=[str(e)], status_code=422)


def handle_invalid_token_error(e):
    return InvalidUsage(messages=[str(e)], status_code=422)


def handle_jwt_decode_error(e):
    return InvalidUsage(messages=[str(e)], status_code=422)


def handle_wrong_token_error(e):
    return InvalidUsage(messages=[str(e)], status_code=401)


def handle_revoked_token_error(e):
    return InvalidUsage(messages=[_("Token has been revoked")], status_code=401)


def handle_fresh_token_required(e):
    return InvalidUsage(messages=[_("Fresh token required")], status_code=401)


def handler_user_load_error(e):
    # The identity is already saved before this exception was raised,
    # otherwise a different exception would be raised, which is why we
    # can safely call get_jwt_identity() here
    identity = get_jwt_identity()
    return InvalidUsage(
        messages=[_("Error loading the user {}").format(identity)], status_code=401
    )


def handle_failed_user_claims_verification(e):
    return InvalidUsage(
        messages=[_("User claims verification failed")], status_code=400
    )


jwt_errors_map = {
    NoAuthorizationError.__name__: {
        "handler": handle_auth_error,
        "error": NoAuthorizationError,
    },
    CSRFError.__name__: {"handler": handle_auth_error, "error": CSRFError},
    ExpiredSignatureError.__name__: {
        "handler": handle_expired_error,
        "error": ExpiredSignatureError,
    },
    InvalidHeaderError.__name__: {
        "handler": handle_invalid_header_error,
        "error": InvalidHeaderError,
    },
    InvalidTokenError.__name__: {
        "handler": handle_invalid_token_error,
        "error": InvalidTokenError,
    },
    JWTDecodeError.__name__: {
        "handler": handle_jwt_decode_error,
        "error": JWTDecodeError,
    },
    WrongTokenError.__name__: {
        "handler": handle_wrong_token_error,
        "error": WrongTokenError,
    },
    RevokedTokenError.__name__: {
        "handler": handle_revoked_token_error,
        "error": RevokedTokenError,
    },
    FreshTokenRequired.__name__: {
        "handler": handle_fresh_token_required,
        "error": FreshTokenRequired,
    },
    UserLoadError.__name__: {
        "handler": handler_user_load_error,
        "error": UserLoadError,
    },
    UserClaimsVerificationError.__name__: {
        "handler": handle_failed_user_claims_verification,
        "error": UserClaimsVerificationError,
    },
}
