from marshmallow import fields, pre_load

from task_office.core.schemas.base_schemas import XSchema
from task_office.swagger import API_SPEC


class SearchTaskSchema(XSchema):
    label = fields.Str(required=False, allow_none=False)
    name = fields.Str(required=False, allow_none=False)
    description = fields.Str(required=False)

    class Meta:
        strict = True

    @pre_load
    def preload_data(self, data, **kwargs):
        return data


search_task_schema = SearchTaskSchema()
API_SPEC.components.schema("SearchTaskSchema", schema=SearchTaskSchema)
