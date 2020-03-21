import uuid

from marshmallow import fields, validates_schema
from marshmallow.validate import Length
from marshmallow_enum import EnumField

from task_office.auth import User
from task_office.boards.schemas.search_schemas import SearchUserSchema
from task_office.core.enums import XEnum
from task_office.core.schemas.base_schemas import BaseSchema, ListSchema, XSchema
from task_office.core.schemas.nested_schemas import NestedUserDumpSchema
from task_office.core.validators import PKExists
from task_office.settings import CONFIG


class BoardPutSchema(BaseSchema):
    name = fields.Str(required=True, allow_none=False, validate=[Length(max=255)])
    description = fields.Str(allow_none=True, required=False, default="")
    owner_uuid = fields.UUID(required=True, validate=[PKExists(User, "uuid")])
    is_active = fields.Boolean(default=True)

    class Meta:
        strict = True

    @validates_schema
    def validate_schema(self, data, **kwargs):
        data["owner_uuid"] = str(data.pop("owner_uuid"))


class BoardDumpSchema(BaseSchema):
    name = fields.Str(dump_only=True)
    description = fields.Str(dump_only=True)
    owner = fields.Nested(NestedUserDumpSchema, dump_only=True)
    is_active = fields.Boolean(dump_only=True)

    class Meta:
        strict = True

    @validates_schema
    def validate_schema(self, data, **kwargs):
        data["uuid"] = uuid.UUID(data.pop("uuid")).hex


board_put_schema = BoardPutSchema()
board_dump_schema = BoardDumpSchema()
board_list_dump_schema = BoardDumpSchema(many=True)
CONFIG.API_SPEC.components.schema("BoardPutSchema", schema=BoardPutSchema)
CONFIG.API_SPEC.components.schema("BoardDumpSchema", schema=BoardDumpSchema)


class BoardListQuerySchema(ListSchema):
    class OrderingMap(XEnum):
        pass

    searching = fields.Nested(XSchema, required=False)
    ordering = EnumField(OrderingMap, required=False, by_value=True)

    class Meta:
        strict = True


board_list_query_schema = BoardListQuerySchema()
CONFIG.API_SPEC.components.schema("BoardListQuerySchema", schema=BoardListQuerySchema)


class UserListByBoardQuerySchema(ListSchema):
    SEARCHING_SCHEMA = SearchUserSchema

    class OrderingMap(XEnum):
        pass

    searching = fields.Nested(SEARCHING_SCHEMA, required=False)
    ordering = EnumField(OrderingMap, required=False, by_value=True)

    class Meta:
        strict = True


user_list_by_board_query_schema = UserListByBoardQuerySchema()
CONFIG.API_SPEC.components.schema(
    "UserListByBoardQuerySchema", schema=UserListByBoardQuerySchema
)
