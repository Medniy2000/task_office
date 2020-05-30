# Babel
# https://pythonhosted.org/Flask-Babel/
# ------------------------------------------------------------------------------
from flask import request, g
from flask_babel import Babel

from task_office.settings import app_config

babel = Babel(default_locale=app_config.LOCALE, default_timezone=app_config.TIME_ZONE)


@babel.localeselector
def get_locale():
    # if a user is logged in, use the locale from the user settings
    user = getattr(g, "user", None)
    if user is not None:
        return user.locale
    return request.accept_languages.best_match(list(app_config.LANGUAGES.keys()))


@babel.timezoneselector
def get_timezone():
    user = getattr(g, "user", None)
    if user is not None:
        return user.timezone
