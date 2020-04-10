import logging
import uuid

from marshmallow import Schema, fields, post_dump, post_load
from marshmallow.validate import Range

from task_office.exceptions import InvalidUsage
from task_office.settings import app_config


class XSchema(Schema):
    def _format_error(self, value="", msg_code="", field_name="detail"):
        return {
            field_name: [self.error_messages.get(msg_code, "").format(value=value)],
            "msg_code": msg_code if msg_code in self.error_messages else "",
        }

    def _throw_exception(self, messages, code):
        raise InvalidUsage(messages=messages, status_code=code)

    def throw_error(self, value, key_error, field_name="detail", code=422):
        messages = [self._format_error(value, key_error, field_name)]
        self._throw_exception(messages=messages, code=code)

    def handle_error(self, exc, data, **kwargs):
        """Log and raise our custom exception when (de)serialization fails."""
        errors_data = exc.messages
        logging.error(errors_data)
        messages = []
        for field_name, msgs in errors_data.items():
            formatted_error = self._format_error(field_name=field_name)
            formatted_error[field_name] = msgs
            messages.append(formatted_error)
        self._throw_exception(messages=messages, code=422)


class BaseSchema(XSchema):
    created_at = fields.DateTime(attribute="created_at", dump_only=True)
    updated_at = fields.DateTime(attribute="updated_at", dump_only=True)
    uuid = fields.UUID(dump_only=True)

    @post_dump
    def dump_data(self, data, **kwargs):
        data["uuid"] = uuid.UUID(data.pop("uuid")).hex
        return data


class ListSchema(XSchema):

    limit = fields.Integer(
        default=app_config.DEFAULT_LIMIT_VALUE,
        required=False,
        validate=[Range(min=1, max=app_config.MAX_LIMIT_VALUE)],
    )
    offset = fields.Integer(
        default=app_config.DEFAULT_OFFSET_VALUE, required=False, validate=[Range(min=0)]
    )


list_schema = ListSchema()


class SearchSchema(XSchema):
    FIELDS_MAP = {}

    @post_load
    def post_load_data(self, data, **kwargs):
        res = {}
        for k, v in data.items():
            k_separated = k.split("__")
            key = k_separated[0]
            key_mapped = self.FIELDS_MAP[key]
            lookup = k_separated[1] if "__" in k else ""
            res[key] = {"value": v, "lookup": lookup, "key": key_mapped}
        return res


search_schema = SearchSchema()
