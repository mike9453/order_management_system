#惠中0513新增

# app/routes/products.py
from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt
from app import db
from app.models import Product

bp_prod = Blueprint('products', __name__, url_prefix='/products')

# —— 1. 列出所有商品 ——
@bp_prod.route('', methods=['GET'])
def list_products():

    """
    列出所有商品
    ---
    tags:
      - Products
    responses:
      200:
        description: 取得商品清單
        content:
          application/json:
            schema:
              type: array
              items:
                $ref: '#/components/schemas/Product'
    """
        
    prods = Product.query.order_by(Product.id).all()   # 取得所有商品
    return jsonify([p.to_dict() for p in prods]), 200

# —— 2. 取得單一商品 ——
@bp_prod.route('/<int:pid>', methods=['GET'])
def get_product(pid):

    """
    取得單一商品
    ---
    tags:
      - Products
    parameters:
      - in: path
        name: pid
        schema:
          type: integer
        required: true
        description: 商品 ID
    responses:
      200:
        description: 商品資料
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Product'
      404:
        description: 找不到商品
    """

    p = Product.query.get_or_404(pid)                  # 找不到回 404
    return jsonify(p.to_dict()), 200

# —— 3. 新增商品（僅 Admin） ——
@bp_prod.route('', methods=['POST'])
@jwt_required()
def create_product():
    """
    新增商品（僅 Admin）
    ---
    tags:
      - Products
    security:
      - bearerAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ProductInput'
    responses:
      201:
        description: 商品建立成功
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Product'
      400:
        description: 欄位錯誤
      403:
        description: 權限不足
    """    
    claims = get_jwt()
    if claims.get("role") != "admin":
        abort(403, description="需要管理員權限")

    data = request.get_json() or {}
    # 驗證必填欄位
    for field in ('name', 'price'):
        if field not in data:
            abort(400, description=f"缺少欄位：{field}")

    prod = Product(
        name=data['name'],
        price=data['price'],
        stock=data.get('stock', 0),
        desc=data.get('desc')
    )
    db.session.add(prod)
    db.session.commit()
    return jsonify(prod.to_dict()), 201

# —— 4. 更新商品（僅 Admin） ——
@bp_prod.route('/<int:pid>', methods=['PUT'])
@jwt_required()
def update_product(pid):
    claims = get_jwt()
    if claims.get("role") != "admin":
        abort(403, description="需要管理員權限")

    prod = Product.query.get_or_404(pid)
    data = request.get_json() or {}
    # 只更新有提供的欄位
    prod.name  = data.get('name', prod.name)
    prod.price = data.get('price', prod.price)
    prod.stock = data.get('stock', prod.stock)
    prod.desc  = data.get('desc',  prod.desc)
    db.session.commit()
    return jsonify(prod.to_dict()), 200

# —— 5. 刪除商品（僅 Admin） ——
@bp_prod.route('/<int:pid>', methods=['DELETE'])
@jwt_required()
def delete_product(pid):
    claims = get_jwt()
    if claims.get("role") != "admin":
        abort(403, description="需要管理員權限")

    prod = Product.query.get_or_404(pid)
    db.session.delete(prod)
    db.session.commit()
    return '', 204
