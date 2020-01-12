# coding: utf-8
import uuid

from marshmallow import fields, validates_schema
from marshmallow.validate import Length
from marshmallow_enum import EnumField

from task_office.auth import User
from task_office.auth.schemas import UserSchemaNested
from task_office.core.enums import XEnum
from task_office.core.schemas import BaseSchema, ListInSchema, XSchema
from task_office.core.validators import PK_Exists
from task_office.swagger import API_SPEC


class BoardInSchema(BaseSchema):
    name = fields.Str(required=True, allow_none=False, validate=[Length(max=255)])
    description = fields.Str(allow_none=True, required=False, default="")
    owner_uuid = fields.UUID(required=True, validate=[PK_Exists(User, "uuid")])
    is_active = fields.Boolean(default=True)

    class Meta:
        strict = True

    @validates_schema
    def validate_schema(self, data, **kwargs):
        data["owner_uuid"] = str(data.pop("owner_uuid"))


class BoardOutSchema(BaseSchema):
    name = fields.Str(dump_only=True)
    description = fields.Str(dump_only=True)
    owner = fields.Nested(UserSchemaNested, dump_only=True)
    is_active = fields.Boolean(dump_only=True)

    class Meta:
        strict = True

    @validates_schema
    def validate_schema(self, data, **kwargs):
        data["uuid"] = uuid.UUID(data.pop("uuid")).hex


board_in_schema = BoardInSchema()
board_out_schema = BoardOutSchema()
boards_list_out_schema = BoardOutSchema(many=True)
API_SPEC.components.schema("BoardInSchema", schema=BoardInSchema)
API_SPEC.components.schema("BoardOutSchema", schema=BoardOutSchema)


class BoardInListSchema(ListInSchema):
    class OrderingMap(XEnum):
        pass

    searching = fields.Nested(XSchema, required=False)
    ordering = EnumField(OrderingMap, required=False, by_value=True)

    class Meta:
        strict = True


boards_in_list_schema = BoardInListSchema()
API_SPEC.components.schema("BoardInListSchema", schema=BoardInListSchema)

