from flask import Flask
from flask_caching import Cache

from task_office.settings import app_config


def init_cache(app: Flask):
    cache = Cache(app=app, config=app_config.CACHE)
