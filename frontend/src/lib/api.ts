export const API_URL = "http://localhost:8000";

const TOKEN_KEY = "jobtracker_token";

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token: string) {
  localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken() {
  localStorage.removeItem(TOKEN_KEY);
}

// Igual que fetch, pero agrega el token y detecta sesiones vencidas
export async function apiFetch(path: string, options: RequestInit = {}) {
  const headers = new Headers(options.headers);
  const token = getToken();
  if (token) headers.set("Authorization", `Bearer ${token}`);

  const res = await fetch(`${API_URL}${path}`, { ...options, headers });

  if (res.status === 401) {
    clearToken();
    window.dispatchEvent(new Event("auth:logout"));
  }
  return res;
}