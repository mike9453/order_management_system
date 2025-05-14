from flask import Blueprint, request, jsonify

bp_practice = Blueprint('practice', __name__, url_prefix='/practice')

@bp_practice.route('/ping', methods=['GET'])
def practice_ping():
    """練習版 ping → 回 pong"""
    return 'pong', 200

@bp_practice.route('/calc', methods=['GET'])
def practice_calc():
    """
    練習版計算機
    URL: /practice/calc?a=數字&b=數字
    回傳 JSON：add, subtract, multiply, divide
    """
    a = request.args.get('a')
    b = request.args.get('b')
    if a is None or b is None:
        return jsonify({"error": "請提供 a 與 b"}), 400
    try:
        a = float(a); b = float(b)
    except ValueError:
        return jsonify({"error": "a 和 b 必須是數字"}), 400

    return jsonify({
        "add": a + b,
        "subtract": a - b,
        "multiply": a * b,
        "divide": None if b == 0 else a / b
    }), 200


@bp_practice.route('/echo', methods=['POST'])
def practice_echo():
    """
    練習版 Echo 路由
    接收 JSON，原封不動地再回傳給客戶端
    """
    data = request.get_json()  # 1. 讀取 JSON body，得到 Python dict
    if not data:
        return jsonify({"error": "請提供 JSON body"}), 400
    # 2. 直接把原始 data 再包成 JSON 回傳
    return jsonify({"you_sent": data}), 200
