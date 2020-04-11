from flask import Flask
from flask_jwt_extended import JWTManager

from task_office.utils import jwt_identity, identity_loader


def init_jwt(app: Flask):
    jwt = JWTManager(app=app)
    jwt.user_loader_callback_loader(jwt_identity)
    jwt.user_identity_loader(identity_loader)
