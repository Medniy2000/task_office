import uuid

from marshmallow import fields, validates_schema
from marshmallow.validate import Length
from marshmallow_enum import EnumField

from task_office.boards.schemas.search_schemas import SearchUserSchema
from task_office.core.enums import XEnum
from task_office.core.schemas.base_schemas import BaseSchema, ListSchema, XSchema
from task_office.settings import app_config


class BoardActionsSchema(BaseSchema):
    name = fields.Str(required=True, allow_none=False, validate=[Length(min=1, max=80)])
    description = fields.Str(
        allow_none=False, required=False, default="", validate=[Length(min=0, max=255)]
    )
    is_active = fields.Boolean(default=True)

    class Meta:
        strict = True


class BoardDumpSchema(BaseSchema):
    name = fields.Str(dump_only=True)
    description = fields.Str(dump_only=True)
    is_active = fields.Boolean(dump_only=True)

    class Meta:
        strict = True

    @validates_schema
    def validate_schema(self, data, **kwargs):
        data["uuid"] = uuid.UUID(data.pop("uuid")).hex


board_action_schema = BoardActionsSchema()
board_dump_schema = BoardDumpSchema()
board_list_dump_schema = BoardDumpSchema(many=True)
app_config.API_SPEC.components.schema("BoardActionsSchema", schema=BoardActionsSchema)
app_config.API_SPEC.components.schema("BoardDumpSchema", schema=BoardDumpSchema)


class BoardListQuerySchema(ListSchema):
    class OrderingMap(XEnum):
        pass

    searching = fields.Nested(XSchema, required=False)
    ordering = EnumField(OrderingMap, required=False, by_value=True)

    class Meta:
        strict = True


board_list_query_schema = BoardListQuerySchema()
app_config.API_SPEC.components.schema(
    "BoardListQuerySchema", schema=BoardListQuerySchema
)


class UserListByBoardQuerySchema(ListSchema):
    SEARCHING_SCHEMA = SearchUserSchema

    class OrderingMap(XEnum):
        pass

    searching = fields.Nested(SEARCHING_SCHEMA, required=False)
    ordering = EnumField(OrderingMap, required=False, by_value=True)

    class Meta:
        strict = True


user_list_by_board_query_schema = UserListByBoardQuerySchema()
app_config.API_SPEC.components.schema(
    "UserListByBoardQuerySchema", schema=UserListByBoardQuerySchema
)
