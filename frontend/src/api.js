// frontend/src/api.js
import axios from "axios";

// Match your FastAPI base URL
const API_BASE = "http://localhost:8000";

// ------------------ ATTACK QUERY ------------------
export async function queryAttacks(filters) {
  const res = await axios.post(`${API_BASE}/attacks/query`, filters);
  return res.data;
}

// ------------------ FETCH STATISTICS ------------------
export async function getStats() {
  const res = await axios.get(`${API_BASE}/attacks/stats`);
  return res.data;
}

// ------------------ EXPORT LINKS ------------------
export function getCsvUrl() {
  return `${API_BASE}/attacks/export/csv`;
}

export function getJsonUrl() {
  return `${API_BASE}/attacks/export/json`;
}

// ------------------ DETECT SINGLE URL (OPTIONAL) ------------------
export async function detectUrl(body) {
  const res = await axios.post(`${API_BASE}/detect_url`, body);
  return res.data;
}
