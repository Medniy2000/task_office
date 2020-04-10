from marshmallow import fields

from task_office.core.models.db_models import User
from task_office.core.schemas.base_schemas import SearchSchema
from task_office.settings import app_config


class SearchUserSchema(SearchSchema):
    FIELDS_MAP = {"username": User.username, "email": User.email}

    username = fields.Str(required=False, allow_none=False)
    email = fields.Email(required=False, allow_none=False)

    class Meta:
        strict = True


search_user_schema = SearchUserSchema()
app_config.API_SPEC.components.schema("SearchUserSchema", schema=SearchUserSchema)
