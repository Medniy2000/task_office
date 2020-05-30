import pytest

from task_office.core.models.db_models import Permission
from tests.factories import UserFactory, BoardFactory, PermissionFactory


@pytest.fixture(scope="function")
def func_users(db):
    """A users for the tests."""
    users = UserFactory.create_batch(3)

    class User:
        @staticmethod
        def get_single():
            return users[0]

        @staticmethod
        def get_list():
            return users

    return User()


@pytest.fixture
def ses_boards(session_users):
    """A boards for the tests."""
    user = session_users.get_single()
    boards = BoardFactory.create_batch(3, owner_uuid=str(user.uuid))
    for item in boards:
        PermissionFactory(
            role=Permission.Role.EDITOR.value, user_uuid=user.uuid, board_uuid=item.uuid
        )

    class Board:
        @staticmethod
        def get_single():
            return boards[0]

        @staticmethod
        def get_list():
            return boards

    return Board()


@pytest.fixture(scope="function")
def func_boards(func_users, db):
    """A boards for the tests."""
    user = func_users.get_single()
    boards = BoardFactory.create_batch(5, owner_uuid=str(user.uuid))
    boards = BoardFactory.create_batch(3, owner_uuid=str(user.uuid))
    for item in boards:
        PermissionFactory(
            role=Permission.Role.EDITOR.value, user_uuid=user.uuid, board_uuid=item.uuid
        )
    db.session.commit()

    class Board:
        @staticmethod
        def get_single():
            return boards[0]

        @staticmethod
        def get_list():
            return boards

    return Board()
