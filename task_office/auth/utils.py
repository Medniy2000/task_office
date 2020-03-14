import uuid

from flask_jwt_extended import get_current_user

from task_office.extensions import cache
from task_office.settings import CONFIG


def _get_cached_permissions():
    user = get_current_user()
    perms = dict()
    if user:
        pk = uuid.UUID(user.uuid).hex
        key = f"perms_{pk}"
        perms = cache.get(key, perms, timeout=CONFIG.JWT_ACCESS_TOKEN_EXPIRES.seconds)
        if not perms:
            perms = {uuid.UUID(item.board_uuid).hex: item.role for item in user.perms}
            if perms:
                cache.set(key, perms, timeout=CONFIG.JWT_ACCESS_TOKEN_EXPIRES.seconds)
    return perms


def delete_cached_permissions(user_uuid_hexed):
    key = f"perms_{user_uuid_hexed}"
    return cache.delete(key)
