"""Create an application instance."""

from task_office.app import create_app
from task_office.settings import app_config

app = create_app(app_config)
