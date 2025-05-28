/*
  src/pages/RegisterPage.jsx
  ----
  會員註冊頁面：輸入 username/email/password
*/
import { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import api from "../api";

export default function RegisterPage() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const nav = useNavigate();

  useEffect(() => {
    if (localStorage.getItem("token")) nav("/products");
  }, [nav]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post("/auth/register", { username, email, password });
      alert("註冊成功，請登入");
      nav("/login");
    } catch (err) {
      console.error(err);
      const status = err.response?.status;
      const data = err.response?.data;
      alert(`註冊失敗！\nStatus：${status}\nResponse：${JSON.stringify(data)}`);
    }
  };

  return (
    <div className="container my-5" style={{ maxWidth: 500 }}>
      <h2 className="mb-4">會員註冊</h2>
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
          <label className="form-label">Email：</label>
          <input
            className="form-control"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
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
          註冊
        </button>
        <p className="mt-3 text-center">
          已有帳號？<Link to="/login"> 點此登入</Link>
        </p>
      </form>
    </div>
  );
}
