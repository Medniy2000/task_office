"""Helper utilities and decorators."""


def jwt_identity(identifier):
    from task_office.auth import User

    return User.get_by_id(identifier)


def identity_loader(user):
    return user.id
