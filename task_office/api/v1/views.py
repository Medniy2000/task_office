from flask.blueprints import Blueprint

from task_office.settings import app_config

bp = Blueprint("api_v1", __name__, url_prefix=app_config.API_PREFIX)
