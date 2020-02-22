from typing import Any
from uuid import UUID

from flask import request
from flask_babel import lazy_gettext as _
from flask_sqlalchemy import BaseQuery

from task_office.core.constants import LOOKUP_MAP
from task_office.exceptions import InvalidUsage
from task_office.extensions import db

Model = db.Model


def _query(model: Model, **params) -> BaseQuery:
    return model.query.filter_by(**params)


def non_empty_query_required(model: Model, **params) -> (BaseQuery, Model):
    qs = _query(model, **params)
    obj_first = qs.first()
    if not obj_first:
        raise InvalidUsage(messages=[_("Not found")], status_code=404)
    return qs, obj_first


def empty_query_required(model: Model, **params) -> (BaseQuery, Model):
    qs = _query(model, **params)
    obj_first = qs.first()
    if obj_first:
        raise InvalidUsage(messages=[_("Already exists")], status_code=422)
    return qs, obj_first


def lookup_filter(
    query: BaseQuery, key: str, value: Any, lookup: str = ""
) -> BaseQuery:
    return LOOKUP_MAP.get(lookup, LOOKUP_MAP.get("e"))(query, key, value)


def is_uuid(uuid):
    try:
        UUID(uuid).version
        return True
    except ValueError:
        return False


def validate_request_url_uuid(
    model: Model, key: str, uuid: str, must_exists: bool = False
):
    if not is_uuid(uuid):
        raise InvalidUsage(messages=[_("Not found")], status_code=404)

    request_url_splitted = request.url.split("/")
    if uuid not in request_url_splitted:
        raise InvalidUsage(messages=[_("Not found")], status_code=404)

    if must_exists:
        non_empty_query_required(model, **{key: uuid})
