import pytest
from app import create_app, db

@pytest.fixture
def client():
    """
    全域 client fixture：
    - 建立測試用 Flask app（TESTING 模式）
    - 使用 in-memory SQLite
    - 建立所有資料表
    - 傳回 app.test_client()
    """
    # 建立並設定 app
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    # 建表
    with app.app_context():
        db.create_all()

    # 測試 client
    yield app.test_client()
