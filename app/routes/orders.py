from flask import Blueprint, jsonify, request, abort
from app import db
from app.models import Order, User

bp_orders = Blueprint('orders', __name__, url_prefix='/orders')

@bp_orders.route('', methods=['POST'])
def create_order():
    """
    建立新訂單 (Create a new order)
    ---
    tags:
      - Orders
    consumes:
      - application/json
    parameters:
      - in: body
        name: order
        required: true
        schema:
          type: object
          required:
            - user_id
            - item
            - quantity
            - price
          properties:
            user_id:
              type: integer
              example: 1
              description: 使用者 ID
            item:
              type: string
              example: "Widget"
              description: 商品名稱
            quantity:
              type: integer
              example: 3
              description: 數量
            price:
              type: number
              format: float
              example: 19.99
              description: 單價
    responses:
      201:
        description: 訂單建立成功 (Order created successfully)
      400:
        description: 輸入資料有誤 (Invalid input)
      404:
        description: 找不到指定使用者 (Specified user not found)
    """
    
    data = request.get_json() or {}
    user_id = data.get('user_id')
    item = data.get('item')
    quantity = data.get('quantity')
    price = data.get('price')
    if not all([user_id, item, quantity, price]):
        abort(400, description="需要 user_id, item, quantity, price (user_id, item, quantity and price are required)")
    if not User.query.get(user_id):
        abort(404, description="找不到指定使用者 (Specified user not found)")
    order = Order(user_id=user_id, item=item, quantity=quantity, price=price)
    db.session.add(order)
    db.session.commit()
    return jsonify({
        "id": order.id,
        "user_id": order.user_id,
        "item": order.item,
        "quantity": order.quantity,
        "price": order.price
    }), 201

@bp_orders.route('', methods=['GET'])
def get_orders():
    """
    取得所有訂單 (List all orders)
    ---
    tags:
      - Orders
    responses:
      200:
        description: 訂單列表 (A list of orders)
    """
    orders = Order.query.all()
    result = [{
        "id": o.id,
        "user_id": o.user_id,
        "item": o.item,
        "quantity": o.quantity,
        "price": o.price
    } for o in orders]
    return jsonify(result), 200

@bp_orders.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """
    取得單一訂單 (Retrieve an order by ID)
    ---
    tags:
      - Orders
    parameters:
      - in: path
        name: order_id
        required: true
        schema:
          type: integer
        description: 訂單 ID (Order ID)
    responses:
      200:
        description: 找到訂單 (Order found)
      404:
        description: 找不到訂單 (Order not found)
    """
    o = Order.query.get_or_404(order_id, description="找不到訂單 (Order not found)")
    return jsonify({
        "id": o.id,
        "user_id": o.user_id,
        "item": o.item,
        "quantity": o.quantity,
        "price": o.price
    }), 200

@bp_orders.route('/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    """
    更新訂單資料 (Update an existing order)
    ---
    tags:
      - Orders
    parameters:
      - in: path
        name: order_id
        required: true
        schema:
          type: integer
        description: 訂單 ID (Order ID)
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              item:
                type: string
                description: 商品名稱 (Item name)
              quantity:
                type: integer
                description: 數量 (Quantity)
              price:
                type: number
                format: float
                description: 單價 (Price per unit)
    responses:
      200:
        description: 訂單更新成功 (Order updated successfully)
      404:
        description: 找不到訂單 (Order not found)
    """
    o = Order.query.get_or_404(order_id, description="找不到訂單 (Order not found)")
    data = request.get_json() or {}
    if data.get('item'):
        o.item = data['item']
    if data.get('quantity'):
        o.quantity = data['quantity']
    if data.get('price'):
        o.price = data['price']
    db.session.commit()
    return jsonify({
        "id": o.id,
        "user_id": o.user_id,
        "item": o.item,
        "quantity": o.quantity,
        "price": o.price
    }), 200

@bp_orders.route('/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    """
    刪除訂單 (Delete an order)
    ---
    tags:
      - Orders
    parameters:
      - in: path
        name: order_id
        required: true
        schema:
          type: integer
        description: 訂單 ID (Order ID)
    responses:
      200:
        description: 訂單刪除成功 (Order deleted successfully)
      404:
        description: 找不到訂單 (Order not found)
    """
    o = Order.query.get_or_404(order_id, description="找不到訂單 (Order not found)")
    db.session.delete(o)
    db.session.commit()
    return jsonify({
        "message": "訂單刪除成功 (Order deleted successfully)"
    }), 200