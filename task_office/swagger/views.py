"""Swagger views."""

from flask import Blueprint, jsonify
from flask_swagger_ui import get_swaggerui_blueprint

from task_office.settings import CONFIG

SWAGGER_URL = CONFIG.API_V1_PREFIX + "docs"

API_URL = "/api/v1/docs/open-api"


blueprint = Blueprint("docs", __name__, url_prefix=SWAGGER_URL)

blueprint_swagger = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": CONFIG.PROJECT_NAME}
)


@blueprint.route("/open-api", methods=("get",))
def api_swagger(**kwargs):
    """
    :param kwargs:
    :return:
    """
    data = CONFIG.API_SPEC.to_dict()
    return jsonify(data)
