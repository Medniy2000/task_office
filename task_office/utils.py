# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""


def jwt_identity(payload):
    from task_office.auth import User

    return User.get_by_id(payload)


def identity_loader(user):
    return user.id
