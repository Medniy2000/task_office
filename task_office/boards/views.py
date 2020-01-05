# -*- coding: utf-8 -*-
"""Boards views."""

from flask import Blueprint
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import jwt_required

from .models import Board
from .serializers import board_schema
from ..settings import CONFIG

blueprint = Blueprint("boards", __name__, url_prefix=CONFIG.API_V1_PREFIX + "/boards")


@blueprint.route("", methods=("post",))
@jwt_required
@use_kwargs(board_schema)
@marshal_with(board_schema)
def create_boards(**kwargs):
    data = kwargs
    board = Board(**data)
    board.save()
    return board
