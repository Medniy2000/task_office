"""Boards models."""
from flask_babel import lazy_gettext as _
from sqlalchemy.dialects.postgresql import UUID

from task_office.core.enums import XEnum
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
    owner = relationship("User", backref=db.backref("boards"))
    is_active = Column(db.Boolean(), default=True)

    def __init__(self, *args, **kwargs):
        """Create instance."""
        db.Model.__init__(self, *args, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return "<Board({name!r})>".format(name=self.name)


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
        return "<Permission({})>".format(self.uuid)


class BoardColumn(PKMixin, DTMixin, Model):

    __tablename__ = "columns"
    __table_args__ = (
        db.UniqueConstraint(
            "board_uuid", "name", name="unique_board__board_column_name"
        ),
    )

    name = Column(db.String(120), nullable=False)
    position = Column(db.Integer(), default=0)
    board_uuid = reference_col("boards", pk_name="uuid", nullable=False)
    board = relationship("Board", backref=db.backref("columns"))

    def __init__(self, *args, **kwargs):
        """Create instance."""
        db.Model.__init__(self, *args, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return "<BoardColumn({})>".format(self.uuid)


users_tasks = db.Table(
    "users_tasks",
    Column("task_uuid", UUID, db.ForeignKey("tasks.uuid"), primary_key=True),
    Column("user_uuid", UUID, db.ForeignKey("users.uuid"), primary_key=True),
)


class Task(PKMixin, DTMixin, Model):

    __tablename__ = "tasks"

    class State(XEnum):
        NEW = 1, _("New"), _("New")
        IN_PROCESS = 2, _("In process"), _("In process")
        REJECTED = 3, _("Rejected"), _("Rejected")
        DONE = 4, _("Done"), _("Done")

    expire_at = db.Column(db.DateTime, nullable=True, default=None)
    label = Column(db.String(80), default="")
    name = Column(db.String(120), nullable=False)
    description = Column(db.String(120), nullable=False)
    state = Column(db.Integer(), default=State.NEW.value)
    position = Column(db.Integer(), default=0)

    column_uuid = reference_col("columns", pk_name="uuid", nullable=False)
    column = relationship("BoardColumn", backref=db.backref("tasks"))

    creator_uuid = reference_col("users", pk_name="uuid", nullable=False)
    creator = relationship("User", backref=db.backref("tasks"))

    performers = db.relationship(
        "User",
        secondary=users_tasks,
        lazy="subquery",
        backref=db.backref("tasks_to_perform", lazy=True),
    )

    def __init__(self, *args, **kwargs):
        """Create instance."""
        db.Model.__init__(self, *args, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return "<Task({})>".format(self.uuid)
