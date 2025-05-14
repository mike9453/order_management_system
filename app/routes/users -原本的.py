from flask import Blueprint, jsonify, request, abort
from app import db
from app.models import User

bp_users = Blueprint('users', __name__, url_prefix='/users')

# -------- User CRUD --------
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

    # 1. 欄位驗證
    errors = {}
    if not data.get('username'):
        errors['username'] = ["需要 username (username is required)"]
    if not data.get('email'):
        errors.setdefault('email', []).append("需要 email (email is required)")
    else:
        # 簡單檢查 email 格式
        if '@' not in data['email'] or '.' not in data['email']:
            errors['email'] = ["email 格式不正確 (Invalid email format)"]
            
    # **加上這兩行 debug 印出**
    print("DEBUG DATA>>>", data)
    print("DEBUG ERRORS>>>", errors)

    if errors:
        return jsonify({
            "code": 400,
            "name": "Bad Request",
            "errors": errors
        }), 400

    username = data['username']
    email = data['email']

    # 2. 重複檢查
    if User.query.filter_by(username=username).first():
        return jsonify({
            "code": 400,
            "name": "Bad Request",
            "errors": {
                "username": ["使用者名稱已存在 (username already exists)"]
            }
        }), 400

    # 3. 建立並存檔
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email
    }), 201

@bp_users.route('', methods=['GET'])
def get_users():
    """
    取得所有使用者清單 (List all users)
    ---
    tags:
      - Users
    responses:
      200:
        description: OK
    """
    users = User.query.all()
    result = [{
        "id": u.id,
        "username": u.username,
        "email": u.email
    } for u in users]
    return jsonify(result), 200

@bp_users.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    取得單一使用者 (Get a single user)
    ---
    tags:
      - Users
    parameters:
      - in: path
        name: user_id
        required: true
        schema:
          type: integer
        description: 使用者 ID (User ID)
    responses:
      200:
        description: 找到使用者 (User found)
      404:
        description: 找不到使用者 (User not found)
    """
    u = User.query.get_or_404(user_id, description="找不到使用者 (User not found)")
    return jsonify({
        "id": u.id,
        "username": u.username,
        "email": u.email
    }), 200


@bp_users.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    更新使用者資料 (Update a user)
    ---
    tags:
      - Users
    parameters:
      - in: path
        name: user_id
        required: true
        schema:
          type: integer
        description: 使用者 ID (User ID)
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              username:
                type: string
                description: 新 username (New username)
              email:
                type: string
                description: 新 email (New email)
    responses:
      200:
        description: 使用者更新成功 (User updated successfully)
      404:
        description: 找不到使用者 (User not found)
    """
    u = User.query.get_or_404(user_id, description="找不到使用者 (User not found)")
    data = request.get_json() or {}
    if data.get('username'):
        u.username = data['username']
    if data.get('email'):
        u.email = data['email']
    db.session.commit()
    return jsonify({
        "id": u.id,
        "username": u.username,
        "email": u.email
    }), 200

@bp_users.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    刪除使用者 (Delete a user)
    ---
    tags:
      - Users
    parameters:
      - in: path
        name: user_id
        required: true
        schema:
          type: integer
        description: 使用者 ID (User ID)
    responses:
      200:
        description: 使用者刪除成功 (User deleted successfully)
      404:
        description: 找不到使用者 (User not found)
    """
    u = User.query.get_or_404(user_id, description="找不到使用者 (User not found)")
    db.session.delete(u)
    db.session.commit()
    return jsonify({
        "message": "使用者刪除成功 (User deleted successfully)"
    }), 200
