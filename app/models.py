from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash  # 惠中0513


class User(db.Model):
    __tablename__ = 'users'  # 資料表名稱
    id = db.Column(db.Integer, primary_key=True)  # 使用者唯一識別
    username = db.Column(db.String(64), unique=True, nullable=False)  # 使用者名稱，不能重複也不可為空
    email = db.Column(db.String(120), unique=True, nullable=False)    # 電子郵件，不能重複也不可為空
    created_at = db.Column(db.DateTime, default=datetime.utcnow)      # 註冊時間，預設為當下 UTC 時間

    # 一對多關係：User.orders 會是一個 Order 清單
    orders = db.relationship('Order', backref='user', lazy=True)

    #惠中0512
    password_hash = db.Column(db.String(255), nullable=True)          # 增加密碼hash，存「密碼的雜湊值」，不存明碼
    role       = db.Column(db.String(20), default="user", nullable=False)  # 建立使用者分一般使用者/管理員   

    # ------- 密碼雜湊工具 ------- #設定的密碼會加密，跑安全機制，防止密碼洩漏
    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)
                                  #再次驗證密碼，也是跑安全機制
    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
    #惠中0512

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)  # 訂單唯一識別
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
        # 外鍵，對應 users.id，不可為空
    item = db.Column(db.String(128), nullable=False)    # 商品名稱，不可為空
    quantity = db.Column(db.Integer, nullable=False)    # 數量，不可為空
    price = db.Column(db.Float, nullable=False)         # 單價，不可為空
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
        # 建立訂單的時間，預設為當下 UTC 時間


#惠中0513惠中惠中惠中惠中惠中惠中惠中惠中惠中惠中惠中惠中惠中惠中惠中惠中惠中惠中惠中惠中惠中惠中惠中
class Product(db.Model):
    __tablename__ = 'products'                         # ① 資料表名稱
    id    = db.Column(db.Integer, primary_key=True)    # ② 主鍵
    name  = db.Column(db.String(120), nullable=False, unique=True)  # ③ 商品名稱，不可空、不可重複
    price = db.Column(db.Float,   nullable=False)      # ④ 價格，不可空
    stock = db.Column(db.Integer, default=0)           # ⑤ 庫存，預設 0
    desc  = db.Column(db.Text)                         # ⑥ 商品描述（可空）
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # ⑦ 建立時間

    def to_dict(self):                                 # ⑧ 快速轉 JSON
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock,
            "desc": self.desc,
            "created_at": self.created_at.isoformat()
        }
#惠中0513惠中惠中惠中惠中惠中惠中惠中惠中惠中惠中惠中惠中惠中惠中惠中惠中惠中惠中惠中惠中惠中惠中惠中


class Payment(db.Model):
    __tablename__ = 'payments'
    id          = db.Column(db.Integer, primary_key=True)
    order_id    = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    status      = db.Column(db.String(20), default='initiated')   # initiated / success / failed
    amount      = db.Column(db.Float, nullable=False)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    order = db.relationship('Order', backref='payment', uselist=False)
