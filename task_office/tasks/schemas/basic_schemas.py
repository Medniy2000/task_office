import uuid

from marshmallow import fields, post_dump, validates_schema, pre_load
from marshmallow.validate import Length, Range
from marshmallow_enum import EnumField

from task_office.core.enums import XEnum, OrderingDirection
from task_office.core.models.db_models import BoardColumn, Task
from task_office.core.schemas.base_schemas import BaseSchema, ListSchema, SearchSchema
from task_office.core.schemas.nested_schemas import NestedUserDumpSchema
from task_office.core.validators import PKExists
from task_office.settings import CONFIG
from task_office.swagger import API_SPEC
from task_office.tasks.schemas.search_schemas import SearchTaskSchema


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
        CREATED_AT_ASC = ("-created_at", Task.created_at.asc(), OrderingDirection.ASC)
        CREATED_AT_DESC = ("created_at", Task.created_at.desc(), OrderingDirection.DESC)
        POSITION_ASC = ("-position", Task.position.asc(), OrderingDirection.ASC)
        POSITION_DESC = ("position", Task.position.desc(), OrderingDirection.DESC)

    searching = fields.Nested(SearchTaskSchema, required=False)
    ordering = EnumField(
        OrderingMap,
        required=False,
        by_value=True,
        default=OrderingMap.POSITION_DESC.value,
    )

    class Meta:
        strict = True

    @pre_load
    def preload_data(self, data, **kwargs):
        data["ordering"] = data.get("ordering", self.OrderingMap.POSITION_ASC)
        return data


task_list_query_schema = TaskListQuerySchema()
API_SPEC.components.schema("TaskListQuerySchema", schema=TaskListQuerySchema)


class ColumnWithTasksDumpSchema(BaseSchema):
    name = fields.Str(dump_only=True)
    position = fields.Integer(dump_only=True)
    tasks = fields.Nested(TaskDumpSchema, many=True)

    @post_dump
    def dump_data(self, data, **kwargs):
        data["uuid"] = uuid.UUID(data.pop("uuid")).hex
        return data

    class Meta:
        strict = True


columns_listed_dump_schema = ColumnWithTasksDumpSchema(many=True)
API_SPEC.components.schema(
    "ColumnWithTasksDumpSchema", schema=ColumnWithTasksDumpSchema
)


class TaskListByColumnsQuerySchema(ListSchema):
    class OrderingMap(XEnum):
        POSITION_ASC = ("-position", BoardColumn.position.asc(), OrderingDirection.ASC)
        POSITION_DESC = (
            "position",
            BoardColumn.position.desc(),
            OrderingDirection.DESC,
        )

    searching = fields.Nested(SearchSchema, required=False)
    ordering = EnumField(OrderingMap, required=False, by_value=True)

    class Meta:
        strict = True


task_list_by_columns_query_schema = TaskListByColumnsQuerySchema()
API_SPEC.components.schema(
    "TaskListByColumnsQuerySchema", schema=TaskListByColumnsQuerySchema
)
