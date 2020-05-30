from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


def init_migrate(app: Flask, db: SQLAlchemy):
    migrate = Migrate(app=app, db=db)
