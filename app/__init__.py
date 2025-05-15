# app/__init__.py
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException
from config import Config
from marshmallow import ValidationError
from flask_migrate import Migrate#惠中0512
from flask_jwt_extended import JWTManager#惠中0512

# 建立 SQLAlchemy 物件，待 create_app 時初始化
db = SQLAlchemy()

def create_app():
    """
    應用程式工廠 (Application Factory)
    - 建立並回傳 Flask app
    - 初始化 SQLAlchemy 與 Marshmallow
    - 啟用 Swagger
    - 註冊各資源藍圖 (Blueprint)
    - 註冊全域錯誤處理
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # 惠中0512--- 新增開始 ---
    app.config["JWT_SECRET_KEY"] = "replace-this-with-env"  # 之後改成環境變數
    jwt = JWTManager(app)
    # 惠中0512--- 新增結束 ---    


    db.init_app(app)
    
    migrate = Migrate(app, db)   #惠中0512

    # 啟用 Swagger
    from flasgger import Swagger
    Swagger(app)

    # 載入並註冊各 Blueprint
    from app.routes.main   import bp_main
    from app.routes.users  import bp_users
    from app.routes.orders import bp_orders
    from app.practice.routes import bp_practice
    from app.routes.auth import bp_auth #惠中0513
    from app.routes.products import bp_prod #惠中0513
    from app.routes.payments import bp_pay#惠中0513


    app.register_blueprint(bp_main)
    app.register_blueprint(bp_users)
    app.register_blueprint(bp_orders)
    app.register_blueprint(bp_practice)
    app.register_blueprint(bp_auth)#惠中0513
    app.register_blueprint(bp_prod)#惠中0513
    app.register_blueprint(bp_pay)#惠中0513

    # 處理 Marshmallow 驗證錯誤 → 400
    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        return jsonify({
            "code": 400,
            "name": "Bad Request",
            "errors": e.messages
        }), 400

    # 處理 HTTPException (400/404 等) → 轉為 JSON
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        response = e.get_response()
        response.data = jsonify({
            "code": e.code,
            "name": e.name,
            "message": e.description
        }).data
        response.content_type = "application/json"
        return response

    # 處理其餘未預期錯誤 → 500
    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, HTTPException):
            return handle_http_exception(e)
        return jsonify({
            "code": 500,
            "name": "Internal Server Error",
            "message": str(e)
        }), 500

    return app
