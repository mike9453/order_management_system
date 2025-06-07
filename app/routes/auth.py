from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)
from app import db
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash

bp_auth = Blueprint('auth', __name__, url_prefix='/auth')

# ---------- 註冊 ----------
@bp_auth.route('/register', methods=['POST'])
def register():
    """
    使用者註冊 (Register)
    ---
    tags:
      - Auth
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - username
            - email
            - password
            - role                     # # 修改：新增 role 欄位
          properties:
            username:
              type: string
              example: alice
            email:
              type: string
              format: email
              example: alice@example.com
            password:
              type: string
              example: secret123
            role:                       # # 修改：新增 role 說明
              type: string
              example: admin
    responses:
      201:
        description: 註冊成功，回傳 id, username, email, role & access_token
      400:
        description: 欄位錯誤或重複註冊
    """

    data = request.get_json() or {}
    required = {'username', 'email', 'password', 'role'}  # # 修改：把 role 加入必填
    missing = required - data.keys()
    if missing:
        abort(400, description=f"缺少欄位: {', '.join(missing)}")

    # # 修改：驗證 role 值
    if data['role'] not in ("admin", "user"):
        abort(400, description="role 必須是 'admin' 或 'user'")

    if User.query.filter_by(username=data['username']).first():
        abort(400, description="使用者名稱已存在")
    if User.query.filter_by(email=data['email']).first():
        abort(400, description="Email 已被註冊")

    user = User(
        username=data['username'],
        email=data['email'],
        role=data['role']               # # 修改：把 role 存進 model
    )
    user.password_hash = generate_password_hash(data['password'])
    db.session.add(user)
    db.session.commit()

    token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role}
    )
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,              # # 修改：回傳 role
        "access_token": token
    }), 201

# ---------- 登入 ----------
@bp_auth.route('/login', methods=['POST'])
def login():
    """
    使用者登入 (Login)
    """
    data = request.get_json() or {}
    user = User.query.filter_by(username=data.get('username')).first()
    if not user or not check_password_hash(user.password_hash, data.get('password', '')):
        abort(401, description="帳號或密碼錯誤")

    token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role}
    )
    return jsonify({"access_token": token}), 200

# ---------- 取得目前使用者資訊 ----------
@bp_auth.route('/me', methods=['GET'])
@jwt_required()
def me():
    """
    取得目前登入者資訊 (Get current user info)
    """
    uid = int(get_jwt_identity())
    user = User.query.get_or_404(uid)
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role              # # 修改：回傳 role
    }), 200
