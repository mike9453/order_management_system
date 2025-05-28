// src/utils/auth.js
import api from "../api";
import { AxiosError } from "axios";

/**
 * 嘗試呼叫 /auth/me 拿 userId，
 * 若回 422 / 401，則回傳 null
 */
export async function fetchCurrentUser() {
  const token = localStorage.getItem("token");
  if (!token) return null;

  try {
    const res = await api.get("/auth/me");
    return res.data.id;
  } catch (err) {
    if (
      err instanceof AxiosError &&
      [401, 422].includes(err.response?.status)
    ) {
      return null;
    }
    throw err;
  }
}
