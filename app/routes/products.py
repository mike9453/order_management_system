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
    prods = Product.query.order_by(Product.id).all()   # 取得所有商品
    return jsonify([p.to_dict() for p in prods]), 200

# —— 2. 取得單一商品 ——
@bp_prod.route('/<int:pid>', methods=['GET'])
def get_product(pid):
    p = Product.query.get_or_404(pid)                  # 找不到回 404
    return jsonify(p.to_dict()), 200

# —— 3. 新增商品（僅 Admin） ——
@bp_prod.route('', methods=['POST'])
@jwt_required()
def create_product():
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
