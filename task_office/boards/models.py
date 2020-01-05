# -*- coding: utf-8 -*-
"""Boards models."""
from task_office.core.models.mixins import DTMixin, PKMixin
from task_office.database import Column, Model, db, reference_col, relationship


class Board(PKMixin, DTMixin, Model):

    __tablename__ = "boards"
    __table_args__ = (
        db.UniqueConstraint("name", "owner_uuid", name="unique_name_owner_board"),
    )

    name = Column(db.String(80), nullable=False)
    description = Column(db.String(255), unique=False, nullable=True, index=True)
    owner_uuid = reference_col("users", pk_name="uuid", nullable=False)
    owner = relationship("User", backref=db.backref("boardds"))
    is_active = Column(db.Boolean(), default=True)

    def __init__(self, *args, **kwargs):
        """Create instance."""
        db.Model.__init__(self, *args, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return "<Board({name!r})>".format(name=self.name)
