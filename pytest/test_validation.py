# tests/test_validation.py

def test_user_validation_success(client):
    # 合法欄位：username 與 email 都給正確格式
    resp = client.post("/users", json={
        "username": "charlie",
        "email": "charlie@example.com"
    })
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["username"] == "charlie"


def test_user_validation_missing_fields(client):
    # 缺少 email
    resp = client.post("/users", json={
        "username": "no_email"
    })
    assert resp.status_code == 400
    err = resp.get_json()
    # 假設你的 ValidationError 處理器會把錯誤訊息放在 'errors' 裡
    assert "email" in err.get("errors", {})


def test_user_validation_bad_email_format(client):
    # email 格式不正確
    resp = client.post("/users", json={
        "username": "bad_email",
        "email": "not-an-email"
    })
    assert resp.status_code == 400
    err = resp.get_json()
    assert "email" in err.get("errors", {})


def test_user_role_validation(client):
    """角色欄位驗證與預設值"""
    # 合法角色應建立成功
    resp = client.post(
        "/users",
        json={"username": "sell", "email": "sell@example.com", "role": "seller"}
    )
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["role"] == "seller"

    # 不合法的角色應回傳 400
    resp2 = client.post(
        "/users",
        json={"username": "badrole", "email": "badrole@example.com", "role": "invalid"}
    )
    assert resp2.status_code == 400
    err2 = resp2.get_json()
    assert "role" in err2.get("errors", {})
