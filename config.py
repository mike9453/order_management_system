import os

class Config:
    # 從環境變數讀取，容器內會注入 DATABASE_URL 指向 db:3306
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://jenny:1234@localhost/my_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False