// src/pages/LoginPage.jsx
import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../api";

export default function LoginPage({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  // 如果 localStorage 裡已經有 token，直接跳去 /products
  useEffect(() => {
    if (localStorage.getItem("token")) {
      navigate("/products", { replace: true });
    }
  }, [navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // 呼叫後端登入 API，成功的話拿到 access_token
      const res = await api.post("/auth/login", { username, password });
      localStorage.setItem("token", res.data.access_token);

      // 通知 AppRouter 更新 token state
      onLogin();

      // 再導到 /products
      navigate("/products", { replace: true });
    } catch (err) {
      console.error(err);
      const status = err.response?.status;
      const data = err.response?.data;
      alert(`登入失敗！\nStatus：${status}\n回傳：${JSON.stringify(data)}`);
    }
  };

  return (
    <div className="container my-5" style={{ maxWidth: 500 }}>
      <h2 className="mb-4">會員登入</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label className="form-label">使用者名稱：</label>
          <input
            className="form-control"
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div className="mb-3">
          <label className="form-label">密碼：</label>
          <input
            className="form-control"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit" className="btn btn-primary w-100">
          登入
        </button>
        <p className="mt-3 text-center">
          還沒帳號？<Link to="/register">立即註冊</Link>
        </p>
      </form>
    </div>
  );
}
