import datetime
import uuid

import factory
from factory import PostGenerationMethodCall, Sequence
from factory.alchemy import SQLAlchemyModelFactory
from factory.fuzzy import FuzzyChoice, FuzzyDateTime
from pytz import UTC

from task_office.core.models.db_models import User, Board, BoardColumn, Task
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


class BoardColumnFactory(BaseFactory):
    """BoardColumn factory."""

    name = Sequence(lambda n: "BoardColumn Name #{0}".format(n))
    position = Sequence(lambda n: n)

    @factory.post_generation
    def tasks(self, create, extracted, **kwargs):
        if create:
            TaskFactory(column_uuid=self.uuid),
            TaskFactory(column_uuid=self.uuid)

    class Meta:
        """Factory configuration."""

        model = BoardColumn


class TaskFactory(BaseFactory):
    """Task factory."""

    expire_at = FuzzyDateTime(datetime.datetime(2020, 1, 1, tzinfo=UTC))
    label = Sequence(lambda n: "Task Label #{0}".format(n))
    name = Sequence(lambda n: "Task Name #{0}".format(n))
    description = Sequence(lambda n: "Task Description #{0}".format(n))
    state = FuzzyChoice(choices=Task.State.get_values())
    position = Sequence(lambda n: n)
    creator = factory.SubFactory(UserFactory)

    @factory.post_generation
    def set_creator_uuid(self, create, extracted, **kwargs):
        if create:
            self.creator_uuid = self.creator.uuid

    class Meta:
        """Factory configuration."""

        model = Task


class BoardFactory(BaseFactory):
    """Board factory."""

    name = Sequence(lambda n: "Board Name #{0}".format(n))
    description = Sequence(lambda n: "Board Description #{0}".format(n))

    @factory.post_generation
    def columns(self, create, extracted, **kwargs):
        if create:
            BoardColumnFactory(board_uuid=self.uuid)
            BoardColumnFactory(board_uuid=self.uuid)
            BoardColumnFactory(board_uuid=self.uuid)

    class Meta:
        """Factory configuration."""

        model = Board
