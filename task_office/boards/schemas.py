# coding: utf-8
from marshmallow import fields, validates_schema
from marshmallow.validate import Length

from task_office.auth import User
from task_office.core.schemas import BaseSchema
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


board_schema = BoardInSchema()


API_SPEC.components.schema("BoardInSchema", schema=BoardInSchema)
