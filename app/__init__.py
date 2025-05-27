# app/__init__.py
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException
from config import DevelopmentConfig, TestingConfig, ProductionConfig
from marshmallow import ValidationError
from flask_migrate import Migrate#惠中0512
from flask_jwt_extended import JWTManager#惠中0512
import os


# 建立 SQLAlchemy 物件，待 create_app 時初始化
db = SQLAlchemy()

# ------------------ Swagger 全域設定 ------------------
swagger_config = {
    "headers": [],
    "specs": [{
        "endpoint": "apispec",
        "route": "/apispec.json",
        "rule_filter": lambda rule: True,   # 所有路由都納入
        "model_filter": lambda tag: True    # 所有 component 都納入
    }],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

template = {
    "swagger": "2.0",
    "info": {
        "title": "Order Management API",
        "version": "1.0",
        "description": "展示後端開發技能的訂單管理系統 API"
    },
    "servers": [
        {"url": "http://localhost:5000", "description": "Development"}
    ],
    "components": {
        "schemas": {
            "User": {
                "type": "object",
                "properties": {
                    "id":       {"type": "integer", "example": 1},
                    "username": {"type": "string",  "example": "alice"},
                    "email":    {"type": "string",  "format": "email", "example": "alice@example.com"}
                }
            },
            "UserInput": {
                "type": "object",
                "required": ["username", "email"],
                "properties": {
                    "username": {"type": "string", "example": "alice"},
                    "email":    {"type": "string", "format": "email", "example": "alice@example.com"}
                }
            },
            # 你可以在這裡繼續加 Products、Orders、Payment… 等 schema

            "Product": {
                "type": "object",
                "properties": {
                    "id":         { "type": "integer", "example": 1 },
                    "name":       { "type": "string",  "example": "T-shirt" },
                    "price":      { "type": "number",  "format": "float", "example": 299.99 },
                    "stock":      { "type": "integer", "example": 100 },
                    "desc":       { "type": "string",  "example": "純棉短袖" },
                    "created_at": { "type": "string",  "format": "date-time" }
                }
            },
            "ProductInput": {
                "type": "object",
                "required": ["name","price"],
                "properties": {
                    "name":  { "type": "string" },
                    "price": { "type": "number", "format": "float" },
                    "stock": { "type": "integer" },
                    "desc":  { "type": "string" }
                }
            },
            "Order": {
                "type": "object",
                "properties": {
                    "id":          { "type": "integer", "example": 1 },
                    "user_id":     { "type": "integer", "example": 1 },
                    "item":        { "type": "string",  "example": "Widget" },
                    "quantity":    { "type": "integer", "example": 3 },
                    "price":       { "type": "number",  "format": "float", "example": 19.99 },
                    "status":      { "type": "string",  "example": "pending" },
                    "total_price": { "type": "number",  "format": "float", "example": 59.97 },
                    "created_at":  { "type": "string",  "format": "date-time" }
                }
            },
            "OrderInput": {
                "type": "object",
                "required": ["user_id","item","quantity","price"],
                "properties": {
                    "user_id":  { "type": "integer" },
                    "item":     { "type": "string" },
                    "quantity": { "type": "integer" },
                    "price":    { "type": "number", "format": "float" }
                }
            },
            "Payment": {
                "type": "object",
                "properties": {
                    "id":         { "type": "integer", "example": 1 },
                    "order_id":   { "type": "integer", "example": 42 },
                    "amount":     { "type": "number",  "format": "float", "example": 59.97 },
                    "status":     { "type": "string",  "example": "success" },
                    "created_at": { "type": "string",  "format": "date-time" }
                }
            }
                        





            
        },
        "securitySchemes": {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "輸入 'Bearer YOUR_TOKEN'"
            }
        }
    },
    "security": [
        {"bearerAuth": []}
    ]
}
# -------------------------------------------------------




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
    env = os.getenv("FLASK_ENV", "development")
    cfg = {
        "development": DevelopmentConfig,
        "testing":    TestingConfig,
        "production": ProductionConfig
    }[env]
    app.config.from_object(cfg)

    # 惠中0512--- 新增開始 ---
    app.config["JWT_SECRET_KEY"] = "replace-this-with-env"  # 之後改成環境變數
    jwt = JWTManager(app)
    # 惠中0512--- 新增結束 ---    


    db.init_app(app)
    
    migrate = Migrate(app, db)   #惠中0512

    # 啟用 Swagger
    from flasgger import Swagger
    Swagger(app, config=swagger_config, template=template)

    # 載入並註冊各 Blueprint
    from app.routes.main   import bp_main
    from app.routes.users  import bp_users
    from app.routes.orders import bp_orders

    from app.routes.auth import bp_auth #惠中0513
    from app.routes.products import bp_prod #惠中0513
    from app.routes.payments import bp_pay#惠中0513


    app.register_blueprint(bp_main)
    app.register_blueprint(bp_users)
    app.register_blueprint(bp_orders)

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
