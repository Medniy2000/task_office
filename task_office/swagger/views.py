"""Swagger views."""

from flask import Blueprint, jsonify
from flask_swagger_ui import get_swaggerui_blueprint

from .specs import API_SPEC
from ..settings import CONFIG

SWAGGER_URL = CONFIG.API_V1_PREFIX + "/docs"

API_URL = "/api/v1/docs/open-api"


blueprint = Blueprint("docs", __name__, url_prefix=CONFIG.API_V1_PREFIX + "/docs")

blueprint_swagger = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": CONFIG.PROJECT_NAME}
)


@blueprint.route("/open-api", methods=("get",))
def api_swagger(**kwargs):
    """
    :param kwargs:
    :return:
    """
    return jsonify(API_SPEC.to_dict())
