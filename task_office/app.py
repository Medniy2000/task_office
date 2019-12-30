# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask

from task_office import commands, auth, swagger
from task_office.exceptions import InvalidUsage
from task_office.extensions import bcrypt, cache, db, migrate, cors, jwt
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
    register_errorhandlers(app)
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


def register_blueprints(app):
    """Register Flask blueprints."""
    origins = app.config.get("CORS_ORIGIN_WHITELIST", "*")
    cors.init_app(auth.views.blueprint, origins=origins)
    app.register_blueprint(auth.views.blueprint)
    if CONFIG.USE_DOCS:
        app.register_blueprint(swagger.views.blueprint_swagger, url_prefix=SWAGGER_URL)
        app.register_blueprint(swagger.views.blueprint)


def register_errorhandlers(app):
    def errorhandler(error):
        response = error.to_json()
        response.status_code = error.status_code
        return response

    app.errorhandler(InvalidUsage)(errorhandler)


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
