# coding: utf-8
import uuid

from marshmallow import fields, post_dump, validates_schema
from marshmallow.validate import Length, Range
from marshmallow_enum import EnumField

from task_office.core.enums import XEnum, OrderingDirection
from task_office.core.models.db_models import BoardColumn, Task
from task_office.core.schemas.base_schemas import BaseSchema, ListSchema, XSchema
from task_office.core.schemas.nested_schemas import NestedUserDumpSchema
from task_office.core.validators import PKExists
from task_office.settings import CONFIG
from task_office.swagger import API_SPEC


class TaskPostSchema(BaseSchema):
    expire_at = fields.DateTime(required=False, allow_none=False, default=None)
    label = fields.Str(
        required=False, allow_none=False, validate=[Length(max=80)], default=""
    )
    name = fields.Str(
        required=True, allow_none=False, validate=[Length(min=1, max=120)]
    )
    description = fields.Str(
        required=False, allow_none=False, validate=[Length(max=120)], default=""
    )
    state = EnumField(
        Task.State,
        required=False,
        allow_none=False,
        by_value=True,
        default=Task.State.NEW.value,
    )
    position = fields.Integer(
        required=True, default=1, allow_none=False, validate=[Range(min=1)]
    )
    column_uuid = fields.UUID(
        required=True, validate=[PKExists(BoardColumn, "uuid")], allow_none=False
    )

    class Meta:
        strict = True

    @validates_schema
    def validate_schema(self, data, **kwargs):
        data["column_uuid"] = str(data.pop("column_uuid"))
        data["state"] = data.pop("state", Task.State.NEW).value


class TaskPutSchema(BaseSchema):
    expire_at = fields.DateTime(required=False, allow_none=False)
    label = fields.Str(required=False, allow_none=False, validate=[Length(max=80)])
    name = fields.Str(
        required=False, allow_none=False, validate=[Length(min=1, max=120)]
    )
    description = fields.Str(
        required=False, allow_none=False, validate=[Length(max=120)]
    )
    state = EnumField(Task.State, required=False, allow_none=False, by_value=True)
    position = fields.Integer(required=False, allow_none=False, validate=[Range(min=1)])
    column_uuid = fields.UUID(
        required=True, validate=[PKExists(BoardColumn, "uuid")], allow_none=False
    )

    class Meta:
        strict = True

    @validates_schema
    def validate_schema(self, data, **kwargs):
        data["column_uuid"] = str(data.pop("column_uuid"))
        state = data.get("state", None)
        if state is not None:
            data["state"] = state.value


class TaskDumpSchema(BaseSchema):
    expire_at = fields.DateTime(
        attribute="expire_at", dump_only=True, format=CONFIG.API_DATETIME_FORMAT
    )
    label = fields.Str(dump_only=True)
    name = fields.Str(dump_only=True)
    description = fields.Str(dump_only=True)
    state = fields.Integer(dump_only=True)
    position = fields.Integer(dump_only=True)
    column_uuid = fields.UUID(dump_only=True)
    performers = NestedUserDumpSchema(many=True)

    @post_dump
    def dump_data(self, data, **kwargs):
        data["uuid"] = uuid.UUID(data.pop("uuid")).hex
        data["column_uuid"] = uuid.UUID(data.pop("column_uuid")).hex
        return data

    class Meta:
        strict = True


task_post_schema = TaskPostSchema()
task_put_schema = TaskPutSchema()
task_dump_schema = TaskDumpSchema()
tasks_listed_dump_schema = TaskDumpSchema(many=True)
API_SPEC.components.schema("TaskPostSchema", schema=TaskPostSchema)
API_SPEC.components.schema("TaskPutSchema", schema=TaskPutSchema)
API_SPEC.components.schema("TaskDumpSchema", schema=TaskDumpSchema)


class TaskListQuerySchema(ListSchema):
    class OrderingMap(XEnum):
        CREATED_AT_ASC = (
            "-created_at",
            BoardColumn.created_at.asc(),
            OrderingDirection.ASC,
        )
        CREATED_AET_DESC = (
            "created_at",
            BoardColumn.created_at.desc(),
            OrderingDirection.DESC,
        )

    searching = fields.Nested(XSchema, required=False)
    ordering = EnumField(OrderingMap, required=False, by_value=True)

    class Meta:
        strict = True


task_list_query_schema = TaskListQuerySchema()
API_SPEC.components.schema("TaskListQuerySchema", schema=TaskListQuerySchema)
