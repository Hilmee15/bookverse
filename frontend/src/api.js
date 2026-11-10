// All calls go through nginx, which proxies /api -> backend:8000 (same origin).
const BASE = "/api";

async function handle(res) {
  if (!res.ok) {
    let detail = res.statusText;
    try {
      const body = await res.json();
      detail = body.detail || detail;
    } catch (_) { /* keep statusText */ }
    const err = new Error(detail);
    err.status = res.status;
    throw err;
  }
  return res.json();
}

export async function fetchBooks() {
  return handle(await fetch(`${BASE}/books`));
}

export async function predict({ query, mode, top_n = 6 }) {
  return handle(
    await fetch(`${BASE}/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, mode, top_n }),
    })
  );
}

export async function fetchHistory(limit = 10) {
  return handle(await fetch(`${BASE}/history?limit=${limit}`));
}
