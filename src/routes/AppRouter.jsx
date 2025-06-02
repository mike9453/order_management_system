// src/routes/AppRouter.jsx
import React, { useState, useEffect } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import HomePage from "../pages/HomePage";
import LoginPage from "../pages/LoginPage";
import RegisterPage from "../pages/RegisterPage";
import ProductsPage from "../pages/ProductsPage";
import ProductForm from "../pages/ProductForm";
import OrdersPage from "../pages/OrdersPage";
import CreateOrderPage from "../pages/CreateOrderPage";

export default function AppRouter() {
  // 用 state 管理 token，才能在登入或登出時觸發重渲染
  const [token, setToken] = useState(localStorage.getItem("token"));

  // 如果 localStorage 在別的分頁被改，這裡也會同步更新
  useEffect(() => {
    const handleStorageChange = () => {
      setToken(localStorage.getItem("token"));
    };
    window.addEventListener("storage", handleStorageChange);
    return () => window.removeEventListener("storage", handleStorageChange);
  }, []);

  // 登入時呼叫，將 localStorage 裡的 token 讀回 state
  const handleLogin = () => {
    const newToken = localStorage.getItem("token");
    setToken(newToken);
  };

  // 登出時呼叫，清除 localStorage 並把 state 也設 null
  const handleLogout = () => {
    localStorage.removeItem("token");
    setToken(null);
  };

  return (
    <BrowserRouter>
      {token && <Navbar onLogout={handleLogout} />}

      <Routes>
        {/* ───────── 根路由 ─────────
            未登入(token 為 null) 時，render HomePage
            已登入(token 不為 null) 時，跳到 /products */}
        <Route
          path="/"
          element={
            token ? <Navigate to="/products" replace /> : <HomePage />
          }
        />

        {/* ───────── 註冊 / 登入 ───────── */}
        <Route
          path="/register"
          element={
            token ? <Navigate to="/products" replace /> : <RegisterPage />
          }
        />
        <Route
          path="/login"
          element={
            token ? (
              <Navigate to="/products" replace />
            ) : (
              <LoginPage onLogin={handleLogin} />
            )
          }
        />

        {/* ───────── 商品路由 ───────── */}
        <Route
          path="/products"
          element={
            token ? <ProductsPage /> : <Navigate to="/login" replace />
          }
        />
        <Route
          path="/products/new"
          element={
            token ? <ProductForm /> : <Navigate to="/login" replace />
          }
        />
        <Route
          path="/products/:id/edit"
          element={
            token ? <ProductForm /> : <Navigate to="/login" replace />
          }
        />

        {/* ───────── 訂單路由 ───────── */}
        <Route
          path="/orders"
          element={
            token ? <OrdersPage /> : <Navigate to="/login" replace />
          }
        />
        <Route
          path="/orders/new"
          element={
            token ? <CreateOrderPage /> : <Navigate to="/login" replace />
          }
        />

        {/* ───────── 其餘路由 ─────────
            如果 URL 不符合以上任一條，則：
              • 已登入 → 導回 /products
              • 未登入 → 導回 / */}
        <Route
          path="*"
          element={
            token ? (
              <Navigate to="/products" replace />
            ) : (
              <Navigate to="/" replace />
            )
          }
        />
      </Routes>
    </BrowserRouter>
  );
}
