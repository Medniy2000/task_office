import uuid

from marshmallow import fields, validates_schema, post_dump
from marshmallow_enum import EnumField

from task_office.auth import User
from task_office.core.enums import XEnum, OrderingDirection
from task_office.core.models.db_models import Permission
from task_office.core.schemas.base_schemas import BaseSchema, ListSchema, XSchema
from task_office.core.schemas.nested_schemas import NestedUserDumpSchema
from task_office.core.validators import PKExists
from task_office.swagger import API_SPEC


class PermissionQuerySchema(BaseSchema):
    role = EnumField(Permission.Role, required=True, by_value=True)
    user_uuid = fields.UUID(
        required=True, validate=[PKExists(User, "uuid")], allow_none=False
    )

    class Meta:
        strict = True

    @validates_schema
    def validate_schema(self, data, **kwargs):
        data["user_uuid"] = str(data.pop("user_uuid"))
        data["role"] = data.pop("role").value


class PermissionDumpSchema(BaseSchema):
    role = fields.Integer(dump_only=True)
    board_uuid = fields.UUID(dump_only=True)
    user = fields.Nested(NestedUserDumpSchema, dump_only=True)

    @post_dump
    def dump_data(self, data, **kwargs):
        data["board_uuid"] = uuid.UUID(data.pop("board_uuid")).hex
        data["uuid"] = uuid.UUID(data.pop("uuid")).hex
        return data

    class Meta:
        strict = True


permission_query_schema = PermissionQuerySchema()
permission_dump_schema = PermissionDumpSchema()
permission_list_dump_schema = PermissionDumpSchema(many=True)
API_SPEC.components.schema("PermissionInSchema", schema=PermissionQuerySchema)
API_SPEC.components.schema("PermissionOutSchema", schema=PermissionDumpSchema)


class PermissionListQuerySchema(ListSchema):
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

    searching = fields.Nested(XSchema, required=False)
    ordering = EnumField(OrderingMap, required=False, by_value=True)

    class Meta:
        strict = True


permissions_list_query_schema = PermissionListQuerySchema()
API_SPEC.components.schema(
    "PermissionListQuerySchema", schema=PermissionListQuerySchema
)
