# app/routes/payments.py
from flask import Blueprint, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Order, Payment

bp_pay = Blueprint('payments', __name__, url_prefix='/payments')

@bp_pay.route('/<int:order_id>', methods=['POST'])
@jwt_required()
def pay_order(order_id):
    uid = int(get_jwt_identity())
    order = Order.query.get_or_404(order_id)
    if order.user_id != uid:
        abort(403, description="這不是你的訂單")

    if order.status != 'pending':
        abort(400, description="訂單已付款或已取消")

    # —— 模擬付款成功 —— #
    payment = Payment(order_id=order.id, amount=order.total_price, status='success')
    order.status = 'paid'
    db.session.add(payment)
    db.session.commit()

    return jsonify({
        "payment_id": payment.id,
        "order_id":   order.id,
        "amount":     payment.amount,
        "status":     payment.status
    }), 201
