# app/models.py

from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(64), unique=True, nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    orders        = db.relationship('Order', backref='user', lazy=True)
    products      = db.relationship('Product', backref='user', lazy=True)   # # 修改：新增與 Product 的關聯
    password_hash = db.Column(db.String(255), nullable=True)
    role          = db.Column(db.String(20), default="user", nullable=False)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Order(db.Model):
    __tablename__ = 'orders'
    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    order_id   = db.Column(db.String(64), unique=True, nullable=False)   # 前端的 orderId
    customer   = db.Column(db.String(120), nullable=False)               # 前端的 customer
    amount     = db.Column(db.Float, nullable=False)                     # 前端的 amount
    status     = db.Column(db.String(20), default='pending', nullable=False)
    date       = db.Column(db.String(20), nullable=False)                # 前端的 date
    remark     = db.Column(db.Text, nullable=True)                       # 前端的 remark
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "orderId":   self.order_id,
            "customer":  self.customer,
            "amount":    self.amount,
            "status":    self.status,
            "date":      self.date,
            "remark":    self.remark,
            "createdAt": self.created_at.isoformat(),
            "createdBy": self.user.username                            # # 修改：回傳建立者 username
        }


class Product(db.Model):
    __tablename__ = 'products'
    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # # 修改：新增 user_id 欄位
    name        = db.Column(db.String(120), nullable=False, unique=True)
    price       = db.Column(db.Float,   nullable=False)
    stock       = db.Column(db.Integer, default=0)
    desc        = db.Column(db.Text)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id":         self.id,
            "name":       self.name,
            "price":      self.price,
            "stock":      self.stock,
            "desc":       self.desc,
            "createdAt":  self.created_at.isoformat(),
            "createdBy":  self.user.username                            # # 修改：回傳建立者 username
        }


class Payment(db.Model):
    __tablename__ = 'payments'
    id         = db.Column(db.Integer, primary_key=True)
    order_id   = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    status     = db.Column(db.String(20), default='initiated')
    amount     = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    order = db.relationship('Order', backref='payment', uselist=False)
