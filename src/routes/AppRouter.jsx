// src/routes/AppRouter.jsx
import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import LoginPage from "../pages/LoginPage";
import RegisterPage from "../pages/RegisterPage";
import ProductsPage from "../pages/ProductsPage";
import ProductForm from "../pages/ProductForm";
import OrdersPage from "../pages/OrdersPage";
import CreateOrderPage from "../pages/CreateOrderPage";

export default function AppRouter() {
  const token = localStorage.getItem("token");

  return (
    <BrowserRouter>
      {token && <Navbar />}
      <Routes>
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/login" element={<LoginPage />} />

        {/* 商品路由 */}
        <Route
          path="/products"
          element={token ? <ProductsPage /> : <Navigate to="/login" replace />}
        />
        <Route
          path="/products/new"
          element={token ? <ProductForm /> : <Navigate to="/login" replace />}
        />
        <Route
          path="/products/:id/edit"
          element={token ? <ProductForm /> : <Navigate to="/login" replace />}
        />

        {/* 訂單路由 */}
        <Route
          path="/orders"
          element={token ? <OrdersPage /> : <Navigate to="/login" replace />}
        />
        <Route
          path="/orders/new"
          element={
            token ? <CreateOrderPage /> : <Navigate to="/login" replace />
          }
        />

        {/* 預設路由 */}
        <Route
          path="*"
          element={
            token ? (
              <Navigate to="/products" replace />
            ) : (
              <Navigate to="/login" replace />
            )
          }
        />
      </Routes>
    </BrowserRouter>
  );
}
