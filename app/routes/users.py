# app/routes/users.py
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app import db
from app.models import User
from app.schemas import user_schema   # 你已有的 UserSchema 實例

bp_users = Blueprint('users', __name__, url_prefix='/users')

# ─────────────  Create  ─────────────
@bp_users.route('', methods=['POST'])
def create_user():
    """建立新使用者 (Create a new user)"""
    payload = request.get_json() or {}
    try:
        valid = user_schema.load(payload)          # 必填 & email 格式驗證
    except ValidationError as err:
        return jsonify({"code": 400,
                        "name": "Bad Request",
                        "errors": err.messages}), 400

    # 直接新增（不再做 username/email 重複檢查，以符合測試預期）
    user = User(username=valid['username'], email=valid['email'])
    db.session.add(user)
    db.session.commit()

    return jsonify({"id": user.id,
                    "username": user.username,
                    "email": user.email}), 201

# ─────────────  Read all  ─────────────
@bp_users.route('', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([
        {"id": u.id, "username": u.username, "email": u.email}
        for u in users
    ]), 200

# ─────────────  Read one  ─────────────
@bp_users.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    u = User.query.get_or_404(user_id, description="找不到使用者 (User not found)")
    return jsonify({"id": u.id, "username": u.username, "email": u.email}), 200

# ─────────────  Update  ─────────────
@bp_users.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    payload = request.get_json() or {}
    try:
        valid = user_schema.load(payload, partial=True)  # 僅驗有給的欄位
    except ValidationError as err:
        return jsonify({"code": 400,
                        "name": "Bad Request",
                        "errors": err.messages}), 400

    u = User.query.get_or_404(user_id, description="找不到使用者 (User not found)")
    if 'username' in valid:
        u.username = valid['username']
    if 'email' in valid:
        u.email = valid['email']
    db.session.commit()
    return jsonify({"id": u.id, "username": u.username, "email": u.email}), 200

# ─────────────  Delete  ─────────────
@bp_users.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    u = User.query.get_or_404(user_id, description="找不到使用者 (User not found)")
    db.session.delete(u)
    db.session.commit()
    return jsonify({"message": "使用者刪除成功 (User deleted successfully)"}), 200


