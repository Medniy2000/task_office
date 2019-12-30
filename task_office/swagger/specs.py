from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin

from task_office.settings import CONFIG

API_SPEC = APISpec(
    openapi_version="3.0.0",
    title=CONFIG.PROJECT_NAME,
    version="1.0.0",
    info=dict(description="Some Description"),
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

# TODO(Medniy) wait for a DocumentedBlueprint and make urls generation
