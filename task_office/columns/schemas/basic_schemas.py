# coding: utf-8
import uuid

from marshmallow import fields, post_dump
from marshmallow.validate import Length, Range
from marshmallow_enum import EnumField

from task_office.core.enums import XEnum, OrderingDirection
from task_office.core.models.db_models import BoardColumn
from task_office.core.schemas.base_schemas import BaseSchema, ListSchema, XSchema
from task_office.swagger import API_SPEC


class ColumnPostSchema(BaseSchema):
    name = fields.Str(required=True, allow_none=False, validate=[Length(max=120)])
    position = fields.Integer(
        required=True, default=1, allow_none=False, validate=[Range(min=1)]
    )

    class Meta:
        strict = True


class ColumnPutSchema(BaseSchema):
    name = fields.Str(required=False, allow_none=False, validate=[Length(max=120)])
    position = fields.Integer(required=False, allow_none=False, validate=[Range(min=1)])

    class Meta:
        strict = True


class ColumnDumpSchema(BaseSchema):
    name = fields.Str(dump_only=True)
    position = fields.Integer(dump_only=True)
    board_uuid = fields.UUID(dump_only=True)

    @post_dump
    def dump_data(self, data, **kwargs):
        data["board_uuid"] = uuid.UUID(data.pop("board_uuid")).hex
        data["uuid"] = uuid.UUID(data.pop("uuid")).hex
        return data

    class Meta:
        strict = True


column_post_schema = ColumnPostSchema()
column_put_schema = ColumnPutSchema()
column_dump_schema = ColumnDumpSchema()
column_listed_dump_schema = ColumnDumpSchema(many=True)
API_SPEC.components.schema("ColumnPostSchema", schema=ColumnPostSchema)
API_SPEC.components.schema("ColumnPutSchema", schema=ColumnPutSchema)
API_SPEC.components.schema("ColumnDumpSchema", schema=ColumnDumpSchema)


class ColumnListQuerySchema(ListSchema):
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


column_list_query_schema = ColumnListQuerySchema()
API_SPEC.components.schema("ColumnListQuerySchema", schema=ColumnListQuerySchema)
