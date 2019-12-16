# -*- coding: utf-8 -*-
"""Create an application instance."""
from flask.helpers import get_debug_flag

from task_office.app import create_app
from task_office.settings import CONFIG

app = create_app(CONFIG)
