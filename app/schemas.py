# app/schemas.py

from marshmallow import Schema, fields

class UserSchema(Schema):
    # 僅做必填檢查
    username = fields.String(
        required=True,
        error_messages={
            "required": "需要 username (username is required)"
        }
    )
    # 內建 Email 檢查
    email = fields.Email(
        required=True,
        error_messages={
            "required": "需要 email (email is required)",
            "invalid": "email 格式不正確 (Invalid email format)"
        }
    )

# 實例化 schema，用於驗證
user_schema = UserSchema()
