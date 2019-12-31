# -*- coding: utf-8 -*-
"""User models."""
from task_office.core.models.mixins import DTMixin, PKMixin
from task_office.database import Column, Model, db
from task_office.extensions import bcrypt


class User(PKMixin, DTMixin, Model):

    __tablename__ = "users"

    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(255), unique=True, nullable=False, index=True)
    bio = Column(db.String(300), nullable=True)
    phone = Column(db.String(300), nullable=True)
    password = Column(db.Binary(128), nullable=True)
    is_active = Column(db.Boolean(), default=True)
    is_superuser = Column(db.Boolean(), default=False)

    def __init__(self, username, email, password=None, **kwargs):
        """Create instance."""
        db.Model.__init__(self, username=username, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    def __repr__(self):
        """Represent instance as a unique string."""
        return "<User({username!r})>".format(username=self.username)
