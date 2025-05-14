from flask import Blueprint, jsonify, request, abort
from app import db
from app.models import User

bp_users = Blueprint('users', __name__, url_prefix='/users')

@bp_users.route('', methods=['POST'])
def create_user():
    """
    建立新使用者 (Create a new user)
    ---
    tags:
      - Users
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - username
              - email
            properties:
              username:
                type: string
                description: 使用者名稱 (Username)
              email:
                type: string
                description: 電子郵件 (Email)
    responses:
      201:
        description: 使用者建立成功 (User created successfully)
      400:
        description: 請求資料格式或驗證錯誤 (Bad Request)
    """
    data = request.get_json() or {}

    # 手動驗證
    errors = {}
    if not data.get('username'):
        errors['username'] = ["需要 username (username is required)"]
    if not data.get('email'):
        errors['email'] = ["需要 email (email is required)"]
    else:
        if '@' not in data['email'] or '.' not in data['email']:
            errors['email'] = ["email 格式不正確 (Invalid email format)"]

    if errors:
        return jsonify({
            "code": 400,
            "name": "Bad Request",
            "errors": errors
        }), 400

    # 重複檢查
    if User.query.filter_by(username=data['username']).first():
        return jsonify({
            "code": 400,
            "name": "Bad Request",
            "errors": {
                "username": ["使用者名稱已存在 (username already exists)"]
            }
        }), 400

    # 建立並存檔
    user = User(username=data['username'], email=data['email'])
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email
    }), 201

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
