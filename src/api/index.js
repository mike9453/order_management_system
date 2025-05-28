import axios from "axios";

// 建立一個 axios 實例、設定 baseURL
const api = axios.create({
  baseURL: "", // 直接向當前網域（http://localhost:3000）發請求，再透過 proxy 轉到 http://localhost:5000
});

// 請求攔截器：自動夾帶 JWT Token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// 回應攔截器：捕捉 401 就跳回登入
api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      alert(err.response.data.message || "請重新登入");
      localStorage.removeItem("token");
      window.location.href = "/login";
    }
    return Promise.reject(err);
  }
);

export default api;
