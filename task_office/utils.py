# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
from flask_babel import lazy_gettext as _
from task_office.exceptions import InvalidUsage


def jwt_identity(identifier):
    from task_office.auth import User

    return User.get_by_id(identifier)


def identity_loader(user):
    return user.id


def non_empty_query_required(model, **params):
    qs = model.query.filter_by(**params)
    obj_first = qs.first()
    if not obj_first:
        raise InvalidUsage(messages=[_("Not found")], status_code=404)
    return qs, obj_first


def empty_query_required(model, **params):
    qs = model.query.filter_by(**params)
    obj_first = qs.first()
    if obj_first:
        raise InvalidUsage(messages=[_("Already exists")], status_code=422)
    return qs, obj_first