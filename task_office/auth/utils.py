import uuid

from flask_babel import lazy_gettext as _
from flask_jwt_extended import get_current_user

from task_office.exceptions import InvalidUsage
from task_office.extensions import cache
from task_office.settings import CONFIG


def _get_cached_permissions():
    user = get_current_user()
    perms = dict()
    if user:
        pk = uuid.UUID(user.uuid).hex
        key = f"perms_{pk}"
        perms = cache.get(key)
        if not perms:
            perms = {uuid.UUID(item.board_uuid).hex: item.role for item in user.perms}
            if perms:
                cache.set(key, perms, timeout=CONFIG.JWT_ACCESS_TOKEN_EXPIRES.seconds)
    return perms


def reset_cached_permissions(user_uuid_hexed):
    key = f"perms_{user_uuid_hexed}"
    return cache.delete(key)


def permission(required_role: int):
    def decorator(func):
        def wrapper(*args, **kwargs):
            board_uuid = kwargs.get("board_uuid", None)
            perms = _get_cached_permissions()
            current_role = perms.get(board_uuid, 9999999)
            if current_role >= required_role:
                raise InvalidUsage(messages=[_("Not allowed")], status_code=403)
            return func(*args, **kwargs)

        wrapper.__name__ = func.__name__
        return wrapper

    return decorator
