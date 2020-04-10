"""Swagger views."""

from flask import Blueprint, jsonify
from flask_swagger_ui import get_swaggerui_blueprint

from task_office.settings import app_config
from task_office.swagger.api_paths import API_PATHS

SWAGGER_URL = app_config.API_V1_PREFIX + "docs"
API_URL = SWAGGER_URL + "/open-api"


blueprint = Blueprint("docs", __name__, url_prefix=SWAGGER_URL)

blueprint_swagger = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": app_config.PROJECT_NAME}
)


@blueprint.route("/open-api", methods=("get",))
def api_swagger(**kwargs):
    """
    :param kwargs:
    :return:
    """
    data = app_config.API_SPEC.to_dict()
    data["paths"] = API_PATHS
    return jsonify(data)
