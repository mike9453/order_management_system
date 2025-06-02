// src/pages/HomePage.jsx
import React from "react";
import { Link } from "react-router-dom";

export default function HomePage() {
  return (
    <div className="container my-5">
      {/* 上方大標題 */}
      <div className="text-center mb-5">
        <h1 className="display-4">歡迎使用訂單管理系統</h1>
        <p className="lead mt-3">
          這是一個簡易的後台管理介面，您可以在此建立、編輯商品，並管理訂單。
        </p>
      </div>

      {/* 中間卡片區塊 */}
      <div className="row justify-content-center">
        <div className="col-md-8">
          <div className="card shadow-sm">
            <div className="card-body text-center">
              <h2 className="card-title mb-4">請先登入或註冊</h2>
              <p className="card-text mb-4">
                請使用以下按鈕進行登入或註冊，之後即可進入系統開始管理商品與訂單。
              </p>
              <div className="d-flex justify-content-center">
                <Link to="/login" className="btn btn-primary btn-lg me-3">
                  前往登入
                </Link>
                <Link to="/register" className="btn btn-outline-secondary btn-lg">
                  立即註冊
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* 底部說明文字 */}
      <div className="text-center mt-5 text-muted">
        <small>還沒有帳號？請點擊「立即註冊」來建立新帳戶。</small>
      </div>
    </div>
  );
}
