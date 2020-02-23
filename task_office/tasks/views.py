"""Tasks views."""
from datetime import datetime

from flask import Blueprint
from flask_apispec import use_kwargs, marshal_with
from flask_babel import lazy_gettext as _
from flask_jwt_extended import jwt_required, get_current_user
from sqlalchemy import func

from .constants import TASKS_PREFIX
from .schemas.basic_schemas import (
    task_list_query_schema,
    tasks_listed_dump_schema,
    task_post_schema,
    task_dump_schema,
    task_put_schema,
    task_list_by_columns_query_schema,
    columns_listed_dump_schema,
)
from .utils import reset_tasks_ordering
from ..core.helpers.listed_response import listed_response
from ..core.models.db_models import BoardColumn, Board, Task, User
from ..core.utils import validate_request_url_uuid, non_empty_query_required
from ..exceptions import InvalidUsage
from ..extensions import db

blueprint = Blueprint("tasks", __name__, url_prefix=TASKS_PREFIX)


@blueprint.route("/meta", methods=("get",))
@jwt_required
def get_meta_data(board_uuid):
    """
    Additional data for tasks
    """
    validate_request_url_uuid(Board, "uuid", board_uuid, True)
    data = dict()
    data["task_state_choices"] = Task.State.dict_choices()
    data["task_list"] = {
        "ordering_choices": task_list_query_schema.OrderingMap.dict_choices(),
        "searching_choices": list(
            task_list_query_schema.SEARCHING_SCHEMA.FIELDS_MAP.keys()
        ),
    }
    data["task_list_by_columns"] = {
        "ordering_choices": task_list_by_columns_query_schema.OrderingMap.dict_choices(),
        "searching_choices": list(
            task_list_by_columns_query_schema.SEARCHING_SCHEMA.FIELDS_MAP.keys()
        ),
    }
    return data


@blueprint.route("", methods=("post",))
@jwt_required
@use_kwargs(task_post_schema)
@marshal_with(task_dump_schema)
def create_task(board_uuid, **kwargs):
    """
    :param board_uuid:
    :param kwargs:
    :return:
    """

    data = kwargs
    validate_request_url_uuid(Board, "uuid", board_uuid, True)

    # validate max position
    data["position"] = data.get("position", 1)
    position = data["position"]
    if position > 1:
        max_position = db.session.query(func.max(Task.position)).scalar()
        max_position = 1 if max_position is None else max_position + 1
        if position > max_position:
            raise InvalidUsage(
                messages=[_("Must be between {} and {}".format(1, max_position))],
                status_code=422,
                key="position",
            )

    # validate unique task name for board
    q_by_name = (
        BoardColumn.query.filter(board_uuid == board_uuid)
        .join(Task)
        .filter(Task.name == data["name"])
        .first()
    )
    if q_by_name:
        raise InvalidUsage(
            messages=[_("Already exists with value {}".format(data["name"]))],
            status_code=422,
            key="name",
        )

    # set creator(current user) of task
    user = get_current_user()
    user_uuid = str(user.uuid) if user else None
    data["creator_uuid"] = user_uuid

    # getting performers before task save
    if data.get("performers", None):
        performers = User.query.filter(User.uuid.in_(data["performers"])).all()
        data["performers"] = performers

    # save task
    task = Task(**data)
    task.save()

    # reset tasks ordering fo column
    reset_tasks_ordering(task, data["column_uuid"], position)

    return task


@blueprint.route("/<task_uuid>", methods=("put",))
@jwt_required
@use_kwargs(task_put_schema)
@marshal_with(task_dump_schema)
def update_task(board_uuid, task_uuid, **kwargs):
    """
    :param board_uuid:
    :param task_uuid:
    :param kwargs:
    :return:
    """
    data = kwargs
    validate_request_url_uuid(Board, "uuid", board_uuid, True)
    validate_request_url_uuid(Task, "uuid", task_uuid, True)

    # validate max position value
    position = data.get("position", None)
    if position is not None and position > 1:
        max_position = db.session.query(func.max(Task.position)).scalar()
        max_position = 1 if max_position is None else max_position + 1

        if position > max_position:
            raise InvalidUsage(
                messages=[_("Must be between {} and {}.".format(1, max_position))],
                status_code=422,
                key="position",
            )

    # get and check is required instance exists
    task = non_empty_query_required(
        Task, uuid=task_uuid, column_uuid=data["column_uuid"]
    )[1]

    # validate unique task name for board
    name = data.get("name", None)
    if name is not None and name != task.name:
        q_by_name = (
            BoardColumn.query.filter(board_uuid == board_uuid)
            .join(Task)
            .filter(Task.name == data["name"])
            .first()
        )
        if q_by_name:
            raise InvalidUsage(
                messages=[_("Already exists with value {}".format(data["name"]))],
                status_code=422,
                key="name",
            )

    if data:

        # getting performers before task save
        if data.get("performers", None):
            performers = User.query.filter(User.uuid.in_(data["performers"])).all()
            data["performers"] = performers

        old_position = task.position

        task.update(updated_at=datetime.utcnow(), **data)
        task.save()

        if position is not None and position > 1:
            reset_tasks_ordering(task, data["column_uuid"], position, old_position)

    return task


@blueprint.route("", methods=("get",))
@jwt_required
@use_kwargs(task_list_query_schema)
def get_list_tasks(board_uuid, **kwargs):
    """
    :param board_uuid:
    :param kwargs:
    :return:
    """
    data = kwargs

    # Check board_uuid in request_url
    validate_request_url_uuid(Board, "uuid", board_uuid, True)

    tasks = Task.query.join(BoardColumn).filter(BoardColumn.board_uuid == board_uuid)

    # Serialize to paginated response
    data = listed_response.serialize(
        query=tasks, query_params=data, schema=tasks_listed_dump_schema
    )
    return data


@blueprint.route("/by-columns", methods=("get",))
@jwt_required
@use_kwargs(task_list_by_columns_query_schema)
def get_list_tasks_by_columns(board_uuid, **kwargs):
    """
    :param board_uuid:
    :param kwargs:
    :return:
    """
    data = kwargs

    # Check board_uuid in request_url
    validate_request_url_uuid(Board, "uuid", board_uuid, True)

    columns_with_tasks = BoardColumn.query.filter(BoardColumn.board_uuid == board_uuid)
    # Serialize to paginated response
    data = listed_response.serialize(
        query=columns_with_tasks, query_params=data, schema=columns_listed_dump_schema
    )
    return data
