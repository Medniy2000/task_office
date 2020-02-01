# coding: utf-8
import uuid

from marshmallow import fields, post_dump
from marshmallow.validate import Length, Range
from marshmallow_enum import EnumField

from task_office.core.enums import XEnum, OrderingDirection
from task_office.core.models.db_models import BoardColumn
from task_office.core.schemas import BaseSchema, ListInSchema, XSchema
from task_office.swagger import API_SPEC


class ColumnInSchema(BaseSchema):
    name = fields.Str(required=True, allow_none=False, validate=[Length(max=120)])
    position = fields.Integer(required=False, default=0, validate=[Range(min=0)])

    class Meta:
        strict = True


class ColumnOutSchema(BaseSchema):
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


column_in_schema = ColumnInSchema()
column_out_schema = ColumnOutSchema()
columns_list_out_schema = ColumnOutSchema(many=True)
API_SPEC.components.schema("ColumnInSchema", schema=ColumnInSchema)
API_SPEC.components.schema("ColumnOutSchema", schema=ColumnOutSchema)


class ColumnsListInSchema(ListInSchema):
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


columns_in_list_schema = ColumnsListInSchema()
API_SPEC.components.schema("ColumnsListInSchema", schema=ColumnsListInSchema)
