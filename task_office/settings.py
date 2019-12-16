# -*- coding: utf-8 -*-
"""Application configuration."""
import os
from datetime import timedelta


class Config(object):
    """Base configuration."""

    SECRET_KEY = os.environ.get("CONDUIT_SECRET", "secret-key")  # TODO: Change me
    API_V1_PREFIX = "/api/v1"
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    BCRYPT_LOG_ROUNDS = 13
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = "simple"  # Can be "memcached", "redis", etc.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_AUTH_USERNAME_KEY = "email"
    JWT_AUTH_HEADER_PREFIX = "Token"
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
    JWT_HEADER_TYPE = "Token"


class ProdConfig(Config):
    """Production configuration."""

    DEBUG = False
    DATABASE = {
        "DB_NAME": os.environ.get("POSTGRES_DB", "task_office"),
        "DB_USER": os.environ.get("POSTGRES_USER", "task_office_user"),
        "DB_PASSWORD": os.environ.get("POSTGRES_PASSWORD", "task_office_user"),
        "DB_HOST": os.environ.get("POSTGRES_HOST", "127.0.0.1"),
        "DB_PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
    SQLALCHEMY_DATABASE_URI = "postgresql://{username}:{password}@{host}:{db_port}/{db_name}".format(
        username=DATABASE["DB_USER"],
        password=DATABASE["DB_PASSWORD"],
        host=DATABASE["DB_HOST"],
        db_port=DATABASE["DB_PORT"],
        db_name=DATABASE["DB_NAME"],
    )


class DevConfig(Config):
    """Development configuration."""

    DEBUG = True
    # Put the db file in project root
    DATABASE = {
        "DB_NAME": os.environ.get("POSTGRES_DB", "task_office_dev"),
        "DB_USER": os.environ.get("POSTGRES_USER", "task_office_user"),
        "DB_PASSWORD": os.environ.get("POSTGRES_PASSWORD", "task_office_user"),
        "DB_HOST": os.environ.get("POSTGRES_HOST", "127.0.0.1"),
        "DB_PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
    SQLALCHEMY_DATABASE_URI = "postgresql://{username}:{password}@{host}:{db_port}/{db_name}".format(
        username=DATABASE["DB_USER"],
        password=DATABASE["DB_PASSWORD"],
        host=DATABASE["DB_HOST"],
        db_port=DATABASE["DB_PORT"],
        db_name=DATABASE["DB_NAME"],
    )
    CACHE_TYPE = "simple"  # Can be "memcached", "redis", etc.
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(10 ** 6)


class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    DEBUG = True
    DATABASE = {
        "DB_NAME": os.environ.get("POSTGRES_DB", "task_office_test"),
        "DB_USER": os.environ.get("POSTGRES_USER", "task_office_user"),
        "DB_PASSWORD": os.environ.get("POSTGRES_PASSWORD", "task_office_user"),
        "DB_HOST": os.environ.get("POSTGRES_HOST", "127.0.0.1"),
        "DB_PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
    SQLALCHEMY_DATABASE_URI = "postgresql:://{username}:{password}@{host}:{db_port}/{db_name}".format(
        username=DATABASE["DB_USER"],
        password=DATABASE["DB_PASSWORD"],
        host=DATABASE["DB_HOST"],
        db_port=DATABASE["DB_PORT"],
        db_name=DATABASE["DB_NAME"],
    )
    BCRYPT_LOG_ROUNDS = 4


MODE = os.environ.get("MODE")

configurations = {
    "dev": DevConfig,
    "prod": ProdConfig,
    "test": TestConfig
}

CONFIG = configurations.get(MODE, "dev")
