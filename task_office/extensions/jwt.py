from flask import Flask
from flask_jwt_extended import JWTManager


def _jwt_identity(identifier):
    from task_office.auth import User

    return User.get_by_id(identifier)


def _identity_loader(user):
    return user.id


def init_jwt(app: Flask):
    jwt = JWTManager(app=app)
    jwt.user_loader_callback_loader(_jwt_identity)
    jwt.user_identity_loader(_identity_loader)
