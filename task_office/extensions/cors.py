from flask import Flask
from flask_cors import CORS


def init_cors(app: Flask):
    cors = CORS(
        app,
        resources={r"/*": {"origins": app.config.get("CORS_ORIGIN_WHITELIST", "*")}},
    )
