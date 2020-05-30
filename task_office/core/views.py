"""Core views."""
from datetime import datetime

from flask import Blueprint

bp = Blueprint("", __name__, url_prefix="")


@bp.route("/", methods=("get",))
def root():
    return {"datetime": datetime.utcnow()}
