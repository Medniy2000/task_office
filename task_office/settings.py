# -*- coding: utf-8 -*-
"""Application configuration."""
import os
from datetime import timedelta

from environs import Env

env = Env()


class Config(object):
    """Base configuration."""

    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))

    READ_DOT_ENV_FILE = env.bool("FLASK_READ_DOT_ENV_FILE", default=True)
    if READ_DOT_ENV_FILE:
        # OS environment variables take precedence over variables from .env
        env.read_env(os.path.join(PROJECT_ROOT, ".env"))

    FLASK_DEBUG = env.int("FLASK_DEBUG", 0)

    PROJECT_NAME = env.str("PROJECT_NAME", "Task Office")
    SECRET_KEY = env.str("FLASK_SECRET", "secret-key")
    API_V1_PREFIX = "/api/v1"

    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CORS_ORIGIN_WHITELIST = [
        "http://0.0.0.0:4100",
        "http://localhost:4100",
        "http://0.0.0.0:8000",
        "http://localhost:8000",
        "http://0.0.0.0:4200",
        "http://localhost:4200",
        "http://0.0.0.0:4000",
        "http://localhost:4000",
    ]

    # JWT
    JWT_AUTH_USERNAME_KEY = "uuid"
    JWT_AUTH_HEADER_PREFIX = "Bearer"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=env.int("JWT_ACCESS_TOKEN_EXPIRES", 30)
    )
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=env.int("JWT_REFRESH_TOKEN_EXPIRES", 7))
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]

    # DB
    DATABASE = {
        "DB_NAME": env.str("POSTGRES_DB", "task_office"),
        "DB_USER": env.str("POSTGRES_USER", "task_office_user"),
        "DB_PASSWORD": env.str("POSTGRES_PASSWORD", "task_office_user"),
        "DB_HOST": env.str("POSTGRES_HOST", "127.0.0.1"),
        "DB_PORT": env.int("POSTGRES_PORT", "5432"),
    }
    SQLALCHEMY_DATABASE_URI = "postgresql://{username}:{password}@{host}:{db_port}/{db_name}".format(
        username=DATABASE["DB_USER"],
        password=DATABASE["DB_PASSWORD"],
        host=DATABASE["DB_HOST"],
        db_port=DATABASE["DB_PORT"],
        db_name=DATABASE["DB_NAME"],
    )


class ProdConfig(Config):
    """Production configuration."""


class DevConfig(Config):
    """Development configuration."""

    CACHE_TYPE = "simple"  # Can be "memcached", "redis", etc.


MODE = os.environ.get("MODE", default="dev")

configurations = {"dev": DevConfig, "prod": ProdConfig}

CONFIG = configurations.get(MODE)
