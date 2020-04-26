import pytest

from tests.factories import UserFactory, BoardFactory


@pytest.fixture(scope="function")
def func_users(db):
    """A users for the tests."""
    users = UserFactory.create_batch(3)
    db.session.commit()

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
    boards = BoardFactory.create_batch(3)
    for item in boards:
        item.user = user
        item.save()

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
    db.session.commit()

    class Board:
        @staticmethod
        def get_single():
            return boards[0]

        @staticmethod
        def get_list():
            return boards

    return Board()
