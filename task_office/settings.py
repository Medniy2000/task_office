"""Application configuration."""
import os
from datetime import timedelta

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from environs import Env

env = Env()


class Config(object):
    """Base configuration."""

    # Project dirs
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))

    # Environment variables setting
    READ_DOT_ENV_FILE = env.bool("FLASK_READ_DOT_ENV_FILE", default=False)
    if READ_DOT_ENV_FILE:
        # OS environment variables take precedence over variables from .env
        env.read_env(os.path.join(PROJECT_ROOT, ".env"))

    PROJECT_NAME = env.str("PROJECT_NAME", "Task Office")
    SECRET_KEY = env.str("FLASK_SECRET", "secret-key")

    API_V1_PREFIX = "/api/v1/"
    API_DATETIME_FORMAT = "%Y-%m-%d %I:%M:%S"
    USE_DOCS = env.bool("USE_DOCS", False)

    API_SPEC = APISpec(
        openapi_version="3.0.2",
        title=PROJECT_NAME,
        version="1.0.0",
        info=dict(description=f"{PROJECT_NAME} API"),
        plugins=[FlaskPlugin(), MarshmallowPlugin()],
    )

    FLASK_DEBUG = env.int("FLASK_DEBUG", 0)
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    TIME_ZONE = "UTC"
    LANGUAGES = {"ru": "Russian", "en": "English", "uk": "Ukrainian"}
    LOCALE = "en"

    # https://pythonhosted.org/Flask-Babel/
    BABEL_TRANSLATION_DIRECTORIES = os.path.join(PROJECT_ROOT, "translations")

    # Static settings
    STATIC_DIR = os.path.abspath(os.path.join(PROJECT_ROOT, "static"))
    STATIC_URL = API_V1_PREFIX + "/static"

    CORS_ORIGIN_WHITELIST = env.list("CORS_ORIGIN_WHITELIST", [])

    # JWT
    JWT_AUTH_USERNAME_KEY = "uuid"
    JWT_AUTH_HEADER_PREFIX = "Bearer"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=env.int("JWT_ACCESS_TOKEN_EXPIRES", 30)
    )
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=env.int("JWT_REFRESH_TOKEN_EXPIRES", 7))
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]

    # Pagination
    DEFAULT_OFFSET_VALUE = 0
    DEFAULT_LIMIT_VALUE = 15
    MAX_LIMIT_VALUE = 50

    # DB
    SQLALCHEMY_TRACK_MODIFICATIONS = False
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

    CACHE = {
        "CACHE_TYPE": env.str("CACHE_TYPE", "redis"),
        "CACHE_REDIS_HOST": env.str("CACHE_REDIS_HOST"),
        "CACHE_REDIS_PORT": env.int("CACHE_REDIS_PORT"),
        "CACHE_REDIS_PASSWORD": env.str("CACHE_REDIS_PASSWORD"),
        "CACHE_REDIS_DB": env.int("CACHE_REDIS_DB"),
        "CACHE_DEFAULT_TIMEOUT": env.int(
            "CACHE_DEFAULT_TIMEOUT", JWT_ACCESS_TOKEN_EXPIRES.seconds
        ),
        "CACHE_REDIS_URL": "redis://:{password}@{host}:{port}/{db}".format(
            password=env.str("CACHE_REDIS_PASSWORD"),
            host=env.str("CACHE_REDIS_HOST"),
            port=env.str("CACHE_REDIS_PORT"),
            db=env.str("CACHE_REDIS_DB"),
        ),
        "OPTIONS": {"PASSWORD": env.str("CACHE_REDIS_PASSWORD")},
    }


class ProdConfig(Config):
    """Production configuration."""


class DevConfig(Config):
    """Development configuration."""


MODE = os.environ.get("MODE", default="dev")

configurations = {"dev": DevConfig, "prod": ProdConfig}

CONFIG = configurations.get(MODE)
