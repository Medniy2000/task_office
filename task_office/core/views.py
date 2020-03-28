"""Core views."""
from datetime import datetime

from flask import Blueprint

blueprint = Blueprint("", __name__, url_prefix="/")


@blueprint.route("", methods=("get",))
def root():
    return {"datetime": datetime.utcnow()}
