import uuid

from marshmallow import fields, post_dump

from task_office.core.schemas.base_schemas import XSchema
from task_office.swagger import API_SPEC


class NestedUserDumpSchema(XSchema):
    uuid = fields.UUID(dump_only=True)
    username = fields.Str(dump_only=True)
    email = fields.Email(dump_only=True)

    @post_dump
    def dump_data(self, data, **kwargs):
        data["uuid"] = uuid.UUID(data.pop("uuid")).hex
        return data

    class Meta:
        strict = True


nested_user_dump_schema = NestedUserDumpSchema()
nested_user_list_dump_schema = NestedUserDumpSchema(many=True)


class NestedColumnDumpSchema(XSchema):
    uuid = fields.UUID(dump_only=True)
    name = fields.Str(dump_only=True)

    @post_dump
    def dump_data(self, data, **kwargs):
        data["uuid"] = uuid.UUID(data.pop("uuid")).hex
        return data

    class Meta:
        strict = True


nested_column_dump_schema = NestedColumnDumpSchema()


API_SPEC.components.schema("NestedUserSchema", schema=NestedUserDumpSchema)
API_SPEC.components.schema("NestedColumnDumpSchema", schema=NestedColumnDumpSchema)
