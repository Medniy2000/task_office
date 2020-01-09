# coding: utf-8
from flask_babel import lazy_gettext as _
from marshmallow import fields, validates_schema
from marshmallow_enum import EnumField

from task_office.auth import User
from task_office.boards import Board
from task_office.core.enums import XEnum, OrderingDirection
from task_office.core.schemas import BaseSchema, ListInSchema, XSchema
from task_office.core.validators import PK_Exists
from task_office.exceptions import InvalidUsage
from task_office.permissions.models import Permission
from task_office.swagger import API_SPEC


class PermissionInSchema(BaseSchema):
    role = EnumField(Permission.Role, required=True, by_value=True)
    board_uuid = fields.UUID(
        required=True, validate=[PK_Exists(Board, "uuid")], allow_none=False
    )
    user_uuid = fields.UUID(
        required=True, validate=[PK_Exists(User, "uuid")], allow_none=False
    )

    class Meta:
        strict = True

    @validates_schema
    def validate_schema(self, data, **kwargs):
        data["board_uuid"] = str(data.pop("board_uuid"))
        data["user_uuid"] = str(data.pop("user_uuid"))
        data["role"] = data.pop("role").value
        obj = Permission.query.filter_by(
            board_uuid=data["board_uuid"], user_uuid=data["user_uuid"]
        ).first()
        if obj:
            raise InvalidUsage(messages=[_("Already exists")], status_code=422)


class PermissionOutSchema(BaseSchema):
    role = fields.Integer(dump_only=True)
    board_uuid = fields.UUID(dump_only=True)
    user_uuid = fields.UUID(dump_only=True)

    class Meta:
        strict = True


permission_in_schema = PermissionInSchema()
permission_out_schema = PermissionOutSchema()
permission_list_out_schema = PermissionOutSchema(many=True)
API_SPEC.components.schema("PermissionInSchema", schema=PermissionInSchema)
API_SPEC.components.schema("PermissionOutSchema", schema=PermissionOutSchema)


class PermissionInListSchema(ListInSchema):
    class OrderingMap(XEnum):
        CREATED_AT_ASC = (
            "-created_at",
            Permission.created_at.asc(),
            OrderingDirection.ASC,
        )
        CREATED_AET_DESC = (
            "created_at",
            Permission.created_at.desc(),
            OrderingDirection.DESC,
        )

    board_uuid = fields.UUID(
        required=True, validate=[PK_Exists(Board, "uuid")], allow_none=False
    )

    searching = fields.Nested(XSchema, required=False)
    ordering = EnumField(OrderingMap, required=False, by_value=True)

    class Meta:
        strict = True


permissions_in_list_schema = PermissionInListSchema()
API_SPEC.components.schema("PermissionInListSchema", schema=PermissionInListSchema)
