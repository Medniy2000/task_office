"""Create an application instance."""

from task_office.app import create_app
from task_office.settings import CONFIG

app = create_app(CONFIG)
