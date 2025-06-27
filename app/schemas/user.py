from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=2))
    email = fields.Email(required=True)
    phone = fields.Str(required=False, allow_none=True, validate=validate.Length(max=40))
    # 調整允許的角色，與路由邏輯保持一致
    role = fields.Str(validate=validate.OneOf(["admin", "seller", "customer"]))
    is_active = fields.Boolean()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    last_login = fields.DateTime(dump_only=True)

user_schema = UserSchema()