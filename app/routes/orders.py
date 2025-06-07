from flask import Blueprint, jsonify, request, abort
from app import db
from app.models import Order
from flask_jwt_extended import jwt_required, get_jwt_identity

bp_orders = Blueprint('orders', __name__, url_prefix='/orders')

@bp_orders.route('', methods=['POST'])
@jwt_required()
def create_order():
    """
    建立新訂單 (Create a new order)
    前端欄位: orderId, customer, amount, status, date, remark
    """
    data = request.get_json() or {}
    order_id = data.get('orderId')
    customer = data.get('customer')
    amount   = data.get('amount')
    status   = data.get('status')
    date     = data.get('date')
    remark   = data.get('remark')

    if not all([order_id, customer, amount, status, date]):
        abort(400, description="需要 orderId、customer、amount、status、date")

    if Order.query.filter_by(order_id=order_id).first():
        abort(400, description="訂單編號已存在")

    user_id = int(get_jwt_identity())
    order = Order(
        user_id=user_id,
        order_id=order_id,
        customer=customer,
        amount=amount,
        status=status,
        date=date,
        remark=remark
    )
    db.session.add(order)
    db.session.commit()
    return jsonify(order.to_dict()), 201

@bp_orders.route('', methods=['GET'])
@jwt_required()
def get_orders():
    """
    取得目前使用者所有訂單 (List all orders for current user)
    """
    user_id = int(get_jwt_identity())
    orders = Order.query.filter_by(user_id=user_id).all()
    return jsonify([o.to_dict() for o in orders]), 200

@bp_orders.route('/<string:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    """
    取得單一訂單 (Retrieve an order by orderId)
    """
    user_id = int(get_jwt_identity())
    o = Order.query.filter_by(order_id=order_id, user_id=user_id).first()
    if not o:
        abort(404, description="找不到訂單")
    return jsonify(o.to_dict()), 200

@bp_orders.route('/<string:order_id>', methods=['PUT'])
@jwt_required()
def update_order(order_id):
    """
    更新訂單資料 (Update an existing order)
    """
    user_id = int(get_jwt_identity())
    o = Order.query.filter_by(order_id=order_id).first()
    if not o or o.user_id != user_id:
        abort(404, description="找不到或無權限修改此訂單")

    data = request.get_json() or {}
    if 'customer' in data:
        o.customer = data['customer']
    if 'amount' in data:
        o.amount = data['amount']
    if 'status' in data:
        o.status = data['status']
    if 'date' in data:
        o.date = data['date']
    if 'remark' in data:
        o.remark = data['remark']

    db.session.commit()
    return jsonify(o.to_dict()), 200

@bp_orders.route('/<string:order_id>', methods=['DELETE'])
@jwt_required()
def delete_order(order_id):
    """
    刪除訂單 (Delete an order)
    """
    user_id = int(get_jwt_identity())
    o = Order.query.filter_by(order_id=order_id).first()
    if not o or o.user_id != user_id:
        abort(404, description="找不到或無權限刪除此訂單")
    db.session.delete(o)
    db.session.commit()
    return jsonify({"message": "訂單刪除成功"}), 200
