/*
  src/index.js
  ----
  全域載入 Bootstrap 樣式與互動功能
*/
import React from "react";
import ReactDOM from "react-dom/client";
// Bootstrap 全域樣式
import "bootstrap/dist/css/bootstrap.min.css";
// Bootstrap JS Bundle (包含 Popper.js)
import "bootstrap/dist/js/bootstrap.bundle.min";
import AppRouter from "./routes/AppRouter";
import "./index.css";
import App from "./App";
import reportWebVitals from "./reportWebVitals";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <AppRouter />
  </React.StrictMode>
);

reportWebVitals();
