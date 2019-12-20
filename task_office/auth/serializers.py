# coding: utf-8

from marshmallow import fields, post_dump, validates_schema
from marshmallow.validate import Length

from task_office.auth.models import User
from task_office.core.serializers import BaseSchema, XSchema
from task_office.core.validators import Unique


class UserSchema(BaseSchema):
    username = fields.Str(dump_only=True)
    email = fields.Email(dump_only=True)
    bio = fields.Str(dump_only=True)

    @post_dump
    def dump_user(self, data, **kwargs):
        return {"user": data}

    class Meta:
        strict = True


user_schema = UserSchema()
user_schemas = UserSchema(many=True)


class UserSignUpSchema(XSchema):
    error_messages = {"passwords_dismatch": "Passwords do not match"}

    password_confirm = fields.Str(
        required=True, load_only=True, validate=[Length(min=6, max=32)]
    )
    password = fields.Str(
        required=True,
        load_only=True,
        validate=[Length(min=6, max=32)],
        error_messages={"required": "Please provide a name."},
    )
    email = fields.Email(
        required=True, validate=[Length(max=255), Unique(User, "email")]
    )
    username = fields.Str(
        required=True, validate=[Length(min=6, max=80), Unique(User, "username")]
    )

    @validates_schema
    def validate_schema(self, data, **kwargs):
        password_confirm = data["password_confirm"]
        password = data["password"]
        if password != password_confirm:
            self.throw_error(value="", key_error="passwords_dismatch", code=422)

    class Meta:
        strict = True

    @post_dump
    def dump_data(self, data, **kwargs):
        return data


user_signup_schema = UserSignUpSchema()
