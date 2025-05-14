from flask import Blueprint, jsonify, request, abort
from app import db
from app.models import User

bp_users = Blueprint('users', __name__, url_prefix='/users')

@bp_users.route('', methods=['GET'])
def get_users():
    """取得所有使用者清單 (List all users)"""
    users = User.query.all()
    result = [{"id": u.id, "username": u.username, "email": u.email} for u in users]
    return jsonify(result), 200

@bp_users.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """取得單一使用者 (Get a single user)"""
    u = User.query.get_or_404(user_id, description="找不到使用者 (User not found)")
    return jsonify({"id": u.id, "username": u.username, "email": u.email}), 200

@bp_users.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """更新使用者資料 (Update a user)"""
    data = request.get_json() or {}
    # 驗證 email 格式
    errors = {}
    if 'email' in data and ('@' not in data['email'] or '.' not in data['email']):
        errors['email'] = ["email 格式不正確 (Invalid email format)"]
    if errors:
        return jsonify({"code":400,"name":"Bad Request","errors":errors}),400

    u = User.query.get_or_404(user_id, description="找不到使用者 (User not found)")
    if data.get('username'):
        u.username = data['username']
    if data.get('email'):
        u.email = data['email']
    db.session.commit()
    return jsonify({"id":u.id, "username":u.username, "email":u.email}), 200

@bp_users.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """刪除使用者 (Delete a user)"""
    u = User.query.get_or_404(user_id, description="找不到使用者 (User not found)")
    db.session.delete(u)
    db.session.commit()
    return jsonify({"message":"使用者刪除成功 (User deleted successfully)"}), 200
