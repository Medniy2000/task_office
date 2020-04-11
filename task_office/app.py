"""The app module, containing the app factory function."""
from flask import Flask

from task_office import commands, swagger, core
from task_office.api import v1 as api_v1
from task_office.auth.jwt_error_handlers import jwt_errors_map
from task_office.exceptions import InvalidUsage
from task_office.extensions.babel import babel
from task_office.extensions.bcrypt import bcrypt
from task_office.extensions.cors import init_cors
from task_office.extensions.db import db
from task_office.extensions.jwt import init_jwt
from task_office.extensions.migrate import init_migrate
from task_office.settings import app_config
from task_office.swagger import SWAGGER_URL


def create_app(config_object):
    """An application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(
        __name__.split(".")[0],
        static_folder=app_config.STATIC_DIR,
        static_url_path=app_config.STATIC_URL,
    )
    app.url_map.strict_slashes = False
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_error_handlers(app)
    register_shell_context(app)
    register_commands(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)
    babel.init_app(app)
    bcrypt.init_app(app)

    init_jwt(app)
    init_migrate(app, db)
    init_cors(app)


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(api_v1.views.bp)

    # root endpoint
    app.register_blueprint(core.views.bp)

    if app_config.USE_DOCS:
        app.register_blueprint(swagger.views.bp_swagger, url_prefix=SWAGGER_URL)
        app.register_blueprint(swagger.views.bp)


def register_error_handlers(app):
    def error_handler(error):
        response = error.to_json()
        response.status_code = error.status_code
        return response

    app.errorhandler(InvalidUsage)(error_handler)

    # register errors(wrapped) for jwt extended custom
    def jwt_error_handler(error):
        wrapped_error_handler = jwt_errors_map[str(error.__class__.__name__)]["handler"]
        unwrapped_error = wrapped_error_handler(error)
        return error_handler(unwrapped_error)

    [
        app.errorhandler(payload["error"])(jwt_error_handler)
        for error_name, payload in jwt_errors_map.items()
    ]


def register_shell_context(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {
            "db": db,
            # 'Article': articles.models.Article,
        }

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
