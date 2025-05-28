// src/pages/OrdersPage.jsx
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";
import { fetchCurrentUser } from "../utils/auth";
import { Link } from "react-router-dom";

export default function OrdersPage() {
  const navigate = useNavigate();
  const [orders, setOrders] = useState([]);
  const [products, setProducts] = useState([]);
  const [userId, setUserId] = useState(null);
  const [expanded, setExpanded] = useState({});

  const fetchOrders = async () => {
    try {
      const res = await api.get("/orders");
      setOrders(res.data);
    } catch (err) {
      console.error("抓訂單列表失敗：", err);
    }
  };

  useEffect(() => {
    async function init() {
      const uid = await fetchCurrentUser();
      if (!uid) return navigate("/login", { replace: true });
      setUserId(uid);

      try {
        const [uo, pu] = await Promise.all([
          api.get("/orders"),
          api.get("/products"),
        ]);
        setOrders(uo.data);
        setProducts(pu.data);
      } catch (err) {
        console.error("初始化訂單/商品失敗", err);
        alert("載入訂單或商品資料時發生錯誤，請稍候再試");
      }
    }
    init();
  }, [navigate]);

  const handleDelete = async (orderId) => {
    if (!window.confirm(`確定要刪除訂單 #${orderId}？`)) return;
    try {
      await api.delete(`/orders/${orderId}`);
      alert(`訂單 #${orderId} 已刪除`);
      fetchOrders();
    } catch (err) {
      console.error("刪除訂單失敗：", err);
      alert("刪除訂單失敗");
    }
  };

  const toggleExpand = (orderId) => {
    setExpanded((prev) => ({ ...prev, [orderId]: !prev[orderId] }));
  };

  return (
    <div>
      <h2>
        訂單管理
        <Link to="/orders/new" style={{ marginLeft: "1rem" }}>
          建立訂單
        </Link>
      </h2>

      <ul style={{ listStyle: "none", padding: 0 }}>
        {orders.map((o) => (
          <li
            key={o.id}
            style={{
              marginBottom: "0.5rem",
              border: "1px solid #ddd",
              borderRadius: "4px",
              padding: "0.5rem",
            }}
          >
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
              }}
            >
              <div>
                <strong>訂單 #{o.id}</strong> — 狀態：{o.status}
              </div>
              <div>
                <button
                  onClick={() => toggleExpand(o.id)}
                  style={{ marginRight: "0.5rem" }}
                >
                  {expanded[o.id] ? "收合" : "顯示詳細"}
                </button>
                <button onClick={() => handleDelete(o.id)}>刪除</button>
              </div>
            </div>

            {expanded[o.id] && (
              <div
                style={{
                  marginTop: "0.5rem",
                  padding: "0.5rem",
                  background: "#f9f9f9",
                  borderRadius: "4px",
                }}
              >
                <h4>商品明細：</h4>
                <table style={{ width: "100%", borderCollapse: "collapse" }}>
                  <thead>
                    <tr>
                      <th style={{ border: "1px solid #ccc", padding: "4px" }}>
                        商品名稱
                      </th>
                      <th style={{ border: "1px solid #ccc", padding: "4px" }}>
                        數量
                      </th>
                      <th style={{ border: "1px solid #ccc", padding: "4px" }}>
                        單價
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {(o.items || []).map((it, idx) => {
                      // 透過 product_id 找到名稱
                      const prod = products.find((p) => p.id === it.product_id);
                      return (
                        <tr key={idx}>
                          <td
                            style={{ border: "1px solid #ccc", padding: "4px" }}
                          >
                            {prod?.name ?? "未知商品"}
                          </td>
                          <td
                            style={{ border: "1px solid #ccc", padding: "4px" }}
                          >
                            {it.quantity}
                          </td>
                          <td
                            style={{ border: "1px solid #ccc", padding: "4px" }}
                          >
                            {it.price}
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>

                <div
                  style={{
                    marginTop: "0.5rem",
                    display: "flex",
                    justifyContent: "flex-end",
                    gap: "1rem",
                    fontWeight: "bold",
                  }}
                >
                  {(() => {
                    const list = o.items || [];
                    const totalQty = list.reduce(
                      (sum, it) => sum + it.quantity,
                      0
                    );
                    const totalAmt = list.reduce(
                      (sum, it) => sum + it.quantity * it.price,
                      0
                    );
                    return (
                      <>
                        <div>總數量：{totalQty}</div>
                        <div>總金額：{totalAmt}</div>
                      </>
                    );
                  })()}
                </div>
              </div>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
