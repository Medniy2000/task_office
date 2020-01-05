# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask
from task_office.auth.jwt_error_handlers import jwt_errors_map

from task_office import commands, auth, swagger, boards
from task_office.exceptions import InvalidUsage
from task_office.extensions import bcrypt, cache, db, migrate, cors, jwt, babel
from task_office.settings import CONFIG
from task_office.swagger import SWAGGER_URL


def create_app(config_object):
    """An application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(
        __name__.split(".")[0],
        static_folder=CONFIG.STATIC_DIR,
        static_url_path=CONFIG.STATIC_URL,
    )
    app.url_map.strict_slashes = False
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_error_handlers(app)
    register_shellcontext(app)
    register_commands(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    babel.init_app(app)


def register_blueprints(app):
    """Register Flask blueprints."""
    origins = app.config.get("CORS_ORIGIN_WHITELIST", "*")
    cors.init_app(auth.views.blueprint, origins=origins)
    app.register_blueprint(auth.views.blueprint)
    app.register_blueprint(boards.views.blueprint)
    if CONFIG.USE_DOCS:
        app.register_blueprint(swagger.views.blueprint_swagger, url_prefix=SWAGGER_URL)
        app.register_blueprint(swagger.views.blueprint)


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


def register_shellcontext(app):
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
