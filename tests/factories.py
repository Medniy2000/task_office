import uuid

from factory import PostGenerationMethodCall, Sequence
from factory.alchemy import SQLAlchemyModelFactory

from task_office.core.models.db_models import User, Board
from task_office.extensions.db import db as _db


class BaseFactory(SQLAlchemyModelFactory):
    """Base factory."""

    uuid = Sequence(lambda n: uuid.uuid4().hex)

    class Meta:
        """Factory configuration."""

        abstract = True
        sqlalchemy_session = _db.session


USER_FACTORY_DEFAULT_PASSWORD = "password"


class UserFactory(BaseFactory):
    """User factory."""

    username = Sequence(lambda n: "user{0}".format(n))
    email = Sequence(lambda n: "user{0}@example.com".format(n))
    password = PostGenerationMethodCall("set_password", USER_FACTORY_DEFAULT_PASSWORD)

    class Meta:
        """Factory configuration."""

        model = User


class BoardFactory(BaseFactory):
    """Board factory."""

    name = Sequence(lambda n: "Board Name #{0}".format(n))
    description = Sequence(lambda n: "Board Description #{0}".format(n))

    class Meta:
        """Factory configuration."""

        model = Board
