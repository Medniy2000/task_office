import pytest

from tests.factories import UserFactory, BoardFactory


@pytest.fixture(scope="function")
def function_users(db):
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
def session_boards(session_users):
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
def function_boards(function_users, db):
    """A boards for the tests."""
    user = function_users.get_single()
    boards = BoardFactory.create_batch(5, owner_uuid=str(user.uuid))
    db.session.commit()

    class Boardx:
        @staticmethod
        def get_single():
            return boards[0]

        @staticmethod
        def get_list():
            return boards

    return Boardx()