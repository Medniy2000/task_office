import typing
from flask_babel import lazy_gettext as _
from marshmallow import ValidationError
from marshmallow.validate import Validator


class Unique(Validator):
    """Validator which is entity exists by some field."""

    already_exists = _("Already exists with value {}")

    def __init__(self, model: object, field_name: str):

        self.model = model
        self.field_name = field_name

    def _repr_args(self) -> str:
        return "model={!r}, field_name={!r}".format(self.model, self.field_name)

    def _format_error(self, value, message: str) -> str:
        return message.format(value)

    def __call__(self, value) -> typing.Any:
        param = {self.field_name: value}

        obj = self.model.query.filter_by(**param).first()

        if obj:
            message = self.already_exists
            raise ValidationError(self._format_error(value, message))
        return value


class PKExists(Validator):
    """Validator of entity pk."""

    not_found = _("Not found with value {}")

    def __init__(self, model: object, field_name: str = "uuid"):

        self.model = model
        self.field_name = field_name

    def _repr_args(self) -> str:
        return "model={!r}, field_name={!r}".format(self.model, self.field_name)

    def _format_error(self, value, message: str) -> str:
        return message.format(value)

    def __call__(self, value) -> typing.Any:
        param = {self.field_name: str(value)}
        obj = self.model.query.filter_by(**param).first()

        if not obj:
            message = self.not_found
            raise ValidationError(self._format_error(value, message))
        return value
