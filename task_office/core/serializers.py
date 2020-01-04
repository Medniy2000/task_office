import logging

from marshmallow import Schema, fields

from task_office.exceptions import InvalidUsage
from task_office.settings import CONFIG


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
    created_at = fields.DateTime(
        attribute="created_at", dump_only=True, format=CONFIG.API_DATETIME_FORMAT
    )
    updated_at = fields.DateTime(
        attribute="updated_at", dump_only=True, format=CONFIG.API_DATETIME_FORMAT
    )
    uuid = fields.UUID(dump_only=True)

    class Meta:
        strict = True
