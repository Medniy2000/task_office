from flask_babel import lazy_gettext as _
from marshmallow import fields, validates_schema
from marshmallow.validate import Length

from task_office.core.models.db_models import User
from task_office.core.schemas.base_schemas import BaseSchema, XSchema
from task_office.core.validators import Unique
from task_office.settings import app_config


class UserSchema(BaseSchema):
    username = fields.Str(dump_only=True)
    email = fields.Email(dump_only=True)
    bio = fields.Str(dump_only=True)

    class Meta:
        strict = True


user_schema = UserSchema()
user_schemas = UserSchema(many=True)


class UserSignUpSchema(XSchema):
    error_messages = {"passwords_dismatch": _("Passwords do not match")}

    password_confirm = fields.Str(
        required=True, load_only=True, validate=[Length(min=6, max=32)]
    )
    password = fields.Str(
        required=True, load_only=True, validate=[Length(min=6, max=32)]
    )
    email = fields.Email(
        required=True, validate=[Length(max=255), Unique(User, "email")]
    )
    username = fields.Str(
        required=True, validate=[Length(min=3, max=80), Unique(User, "username")]
    )

    @validates_schema
    def validate_schema(self, data, **kwargs):
        password_confirm = data["password_confirm"]
        password = data["password"]
        if password != password_confirm:
            self.throw_error(value="", key_error="passwords_dismatch", code=422)

    class Meta:
        strict = True


user_signup_schema = UserSignUpSchema()


class UserSignInSchema(XSchema):
    error_messages = {"usr_not_found": _("User not found")}

    password = fields.Str(
        required=True, load_only=True, validate=[Length(min=6, max=32)]
    )
    email = fields.Email(required=True, load_only=True, validate=[Length(max=255)])

    @validates_schema
    def validate_schema(self, data, **kwargs):
        email = data["email"]
        password = data["password"]
        user = User.query.filter_by(email=email).first()
        if user is not None and user.check_password(password):
            data["user"] = user
        else:
            self.throw_error(value="", key_error="usr_not_found", code=422)

    class Meta:
        strict = True


user_signin_schema = UserSignInSchema()


class TokenSchema(XSchema):
    token = fields.Str()
    lifetime = fields.Integer()


class SignedTokensSchema(XSchema):
    access = fields.Nested(TokenSchema)
    refresh = fields.Nested(TokenSchema)
    header_type = fields.Str()
    time_zone_info = fields.Str()


class RefreshedAccessTokenSchema(XSchema):
    access = fields.Nested(TokenSchema)
    time_zone_info = fields.Str()


class SignedSchema(XSchema):
    tokens = fields.Nested(SignedTokensSchema)
    user = fields.Nested(UserSchema)


signed_schema = SignedSchema()
signed_tokens_schema = SignedTokensSchema()
refreshed_access_tokens_schema = RefreshedAccessTokenSchema()
token_schema = TokenSchema()


app_config.API_SPEC.components.schema("UserSchema", schema=UserSchema)
app_config.API_SPEC.components.schema("UserSignInSchema", schema=UserSignInSchema)
app_config.API_SPEC.components.schema("UserSignUpSchema", schema=UserSignUpSchema)
app_config.API_SPEC.components.schema("TokenSchema", schema=TokenSchema)
app_config.API_SPEC.components.schema("SignedTokensSchema", schema=SignedTokensSchema)
app_config.API_SPEC.components.schema(
    "RefreshedAccessTokenSchema", schema=RefreshedAccessTokenSchema
)
app_config.API_SPEC.components.schema("SignedSchema", schema=SignedSchema)
