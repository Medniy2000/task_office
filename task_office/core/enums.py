from enum import Enum
from flask_babel import lazy_gettext as _


class XEnum(Enum):
    """
    Base Enum for project
    """

    # ADMIN = 0, _('Admin'), _('Approximate quantity: format +/-')
    # EDITOR = 1, _('Editor'), _('Strict, exact quantity: format numeric')

    @classmethod
    def choices(cls):
        return [(tag.name, tag.value) for tag in cls]

    @classmethod
    def dict_choices(cls):
        return [
            {"name": tag.name, "value": tag.value, "description": tag.description}
            for tag in cls
        ]

    @classmethod
    def get_names(cls):
        return [item.name for item in cls]

    @classmethod
    def get_values(cls):
        return [item.value for item in cls]

    def __new__(cls, value, name, description=""):
        member = object.__new__(cls)
        member._value_ = value
        member.fullname = name
        member.description = description
        return member

    def __int__(self):
        return self.value

    def __str__(self):
        return self.value


class OrderingDirection(XEnum):
    ASC = "asc", _("Ascend")
    DESC = "desc", _("Descend")
