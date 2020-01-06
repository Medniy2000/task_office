# -*- coding: utf-8 -*-
"""Permission models."""

from flask_babel import lazy_gettext as _

from task_office.core.enums import XEnum
from task_office.core.models.mixins import DTMixin, PKMixin
from task_office.database import Column, Model, db, reference_col, relationship


class Permission(PKMixin, DTMixin, Model):

    __tablename__ = "permissions"
    __table_args__ = (
        db.UniqueConstraint(
            "board_uuid", "user_uuid", name="unique_board_owner_permission"
        ),
    )

    class Role(XEnum):
        OWNER = 9, _("Owner"), _("Owner of board(creator)")
        EDITOR = 8, _("Editor"), _("Editor of board")
        STAFF = 7, _("Staff"), _("Ordinary user")

    role = Column(db.Integer(), default=Role.STAFF.value)
    user_uuid = reference_col("users", pk_name="uuid", nullable=False)
    user = relationship("User", backref=db.backref("perms"))
    board_uuid = reference_col("boards", pk_name="uuid", nullable=False)
    board = relationship("Board", backref=db.backref("perms"))

    def __init__(self, *args, **kwargs):
        """Create instance."""
        db.Model.__init__(self, *args, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return "<Permission({uuid!r})>".format(name=self.uuid)
