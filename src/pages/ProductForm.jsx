/*
  src/pages/ProductForm.jsx
  ----
  商品表單：新增與編輯共用，包含名稱與價格欄位
*/
import { useState, useEffect } from "react";
import api from "../api";
import { useNavigate, useParams } from "react-router-dom";

export default function ProductForm() {
  const [name, setName] = useState("");
  const [price, setPrice] = useState("");
  const nav = useNavigate();
  const { id } = useParams();

  useEffect(() => {
    if (id) {
      api.get(`/products/${id}`).then((res) => {
        setName(res.data.name);
        setPrice(res.data.price);
      });
    }
  }, [id]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (id) {
        await api.put(`/products/${id}`, { name, price });
      } else {
        await api.post("/products", { name, price });
      }
      nav("/products");
    } catch (err) {
      alert("操作失敗");
    }
  };

  return (
    <div className="container my-5" style={{ maxWidth: 500 }}>
      <h2 className="mb-4">{id ? "編輯商品" : "新增商品"}</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label className="form-label">名稱：</label>
          <input
            className="form-control"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>
        <div className="mb-3">
          <label className="form-label">價格：</label>
          <input
            type="number"
            className="form-control"
            value={price}
            onChange={(e) => setPrice(e.target.value)}
            required
          />
        </div>
        <button type="submit" className="btn btn-primary">
          {id ? "更新" : "新增"}
        </button>
      </form>
    </div>
  );
}
