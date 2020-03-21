from marshmallow import fields

from task_office.core.models.db_models import Task
from task_office.core.schemas.base_schemas import SearchSchema
from task_office.settings import CONFIG


class SearchTaskSchema(SearchSchema):
    FIELDS_MAP = {
        "label": Task.label,
        "name": Task.name,
        "description": Task.description,
        "position": Task.position,
    }

    label = fields.Str(required=False, allow_none=False)
    name = fields.Str(required=False, allow_none=False)
    description = fields.Str(required=False)
    position = fields.Integer(required=False)

    class Meta:
        strict = True


search_task_schema = SearchTaskSchema()
CONFIG.API_SPEC.components.schema("SearchTaskSchema", schema=SearchTaskSchema)
