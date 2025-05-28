/*
  src/components/Navbar.jsx
  ----
  導航列：顯示主要路由與使用者資訊，包含登出按鈕
*/
import { Link, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import api from "../api";

export default function Navbar() {
  const [userName, setUserName] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    async function fetchName() {
      try {
        const res = await api.get("/auth/me");
        setUserName(res.data.username);
      } catch (e) {
        console.error("抓取使用者資訊失敗：", e);
      }
    }
    fetchName();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-light">
      <div className="container-fluid">
        <Link className="navbar-brand" to="/products">
          訂單系統
        </Link>
        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav me-auto mb-2 mb-lg-0">
            <li className="nav-item">
              <Link className="nav-link" to="/products">
                商品列表
              </Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/products/new">
                新增商品
              </Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/orders">
                訂單管理
              </Link>
            </li>
          </ul>
          <span className="navbar-text me-3">你好，{userName}</span>
          <button className="btn btn-outline-secondary" onClick={handleLogout}>
            登出
          </button>
        </div>
      </div>
    </nav>
  );
}
