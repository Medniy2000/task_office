# -*- coding: utf-8 -*-
import datetime as dt
import uuid as uuid

from sqlalchemy import JSON
from sqlalchemy.dialects.postgresql import UUID

from task_office.compat import basestring
from task_office.extensions import db


class PKMixin(object):
    """
    A mixin that adds a surrogate pk(s) fields
    """

    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(UUID, primary_key=True, default=uuid.uuid4().__str__())
    meta = db.Column(JSON, default=dict)

    @classmethod
    def get_by_id(cls, record_id):
        """Get record by ID."""
        if any(
            (
                isinstance(record_id, basestring) and record_id.isdigit(),
                isinstance(record_id, (int, float)),
            )
        ):
            return cls.query.filter_by(id=record_id).first()


class DTMixin(object):
    """
    A mixin that adds a created_at, updated_at fields
    """

    __table_args__ = {"extend_existing": True}

    created_at = db.Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=dt.datetime.utcnow,
        onupdate=dt.datetime.utcnow,
    )
