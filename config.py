import os

class Config:
    # MySQL 資料庫連線字串：
    # 格式：mysql+pymysql://<使用者名稱>:<密碼>@<主機>/<資料庫名稱>
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://jenny:1234@localhost/order_management'
    # 關閉 SQLAlchemy 的修改追蹤功能，可減少不必要的記憶體與效能負擔
    SQLALCHEMY_TRACK_MODIFICATIONS = False
