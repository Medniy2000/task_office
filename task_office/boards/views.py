# -*- coding: utf-8 -*-
"""Boards views."""

from flask import Blueprint
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import jwt_required

from .models import Board
from .schemas import board_schema
from ..settings import CONFIG

BOARDS_PREFIX = CONFIG.API_V1_PREFIX + "/boards"
BOARD_RETRIEVE_URL = BOARDS_PREFIX + "/<board_uuid>"

blueprint = Blueprint("boards", __name__, url_prefix=BOARDS_PREFIX)


@blueprint.route("", methods=("post",))
@jwt_required
@use_kwargs(board_schema)
@marshal_with(board_schema)
def create_boards(**kwargs):
    data = kwargs
    board = Board(**data)
    board.save()
    return board
