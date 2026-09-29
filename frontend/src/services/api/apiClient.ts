/**
 * NOVA Hackathon Portal — Centralized API Client
 * Base URL: VITE_API_BASE_URL env var (defaults to http://localhost:8000/api/v1)
 *
 * Handles: Bearer JWT auth, JSON parsing, all HTTP status error cases
 */

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';
export const TOKEN_KEY = 'nova_jwt_token';
export const TOKEN_STORAGE_KEY = TOKEN_KEY;
export const USER_STORAGE_KEY = 'nova_auth_user';

export interface ApiError {
  status: number;
  detail: string;
  isApiError: true;
}

export function isApiError(e: unknown): e is ApiError {
  return typeof e === 'object' && e !== null && (e as ApiError).isApiError === true;
}

export function getStoredToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

export function setStoredToken(token: string): void {
  localStorage.setItem(TOKEN_KEY, token);
}

export function clearStoredToken(): void {
  localStorage.removeItem(TOKEN_KEY);
}

function buildHeaders(): Record<string, string> {
  const h: Record<string, string> = { 'Content-Type': 'application/json' };
  const tok = getStoredToken();
  if (tok) h['Authorization'] = `Bearer ${tok}`;
  return h;
}

async function parseResponse<T>(res: Response): Promise<T> {
  if (res.status === 204) return undefined as unknown as T;

  let body: unknown;
  try { body = await res.json(); } catch { body = { detail: res.statusText || 'Unknown error' }; }

  if (!res.ok) {
    const b = body as any;
    let detail = b?.detail ?? `HTTP ${res.status}`;
    // FastAPI 422 validation error array
    if (Array.isArray(detail)) detail = detail.map((e: any) => `${e.loc?.join('.')}: ${e.msg}`).join(' | ');
    if (typeof detail !== 'string') detail = JSON.stringify(detail);

    // 401 — clear stale token
    if (res.status === 401) clearStoredToken();

    throw { status: res.status, detail, isApiError: true } as ApiError;
  }
  return body as T;
}

export const apiClient = {
  async get<T>(path: string, params?: Record<string, string | number | boolean | undefined>): Promise<T> {
    let url = `${API_BASE_URL}${path}`;
    if (params) {
      const qs = Object.entries(params)
        .filter(([, v]) => v !== undefined && v !== null && v !== '')
        .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(String(v))}`)
        .join('&');
      if (qs) url += `?${qs}`;
    }
    const res = await fetch(url, { method: 'GET', headers: buildHeaders() });
    return parseResponse<T>(res);
  },

  async post<T>(path: string, body?: unknown): Promise<T> {
    const res = await fetch(`${API_BASE_URL}${path}`, {
      method: 'POST',
      headers: buildHeaders(),
      body: body !== undefined ? JSON.stringify(body) : undefined,
    });
    return parseResponse<T>(res);
  },

  async put<T>(path: string, body?: unknown): Promise<T> {
    const res = await fetch(`${API_BASE_URL}${path}`, {
      method: 'PUT',
      headers: buildHeaders(),
      body: body !== undefined ? JSON.stringify(body) : undefined,
    });
    return parseResponse<T>(res);
  },

  async patch<T>(path: string, body?: unknown): Promise<T> {
    const res = await fetch(`${API_BASE_URL}${path}`, {
      method: 'PATCH',
      headers: buildHeaders(),
      body: body !== undefined ? JSON.stringify(body) : undefined,
    });
    return parseResponse<T>(res);
  },

  async delete<T>(path: string): Promise<T> {
    const res = await fetch(`${API_BASE_URL}${path}`, { method: 'DELETE', headers: buildHeaders() });
    return parseResponse<T>(res);
  },

  async downloadCsv(path: string): Promise<string> {
    const h: HeadersInit = {};
    const tok = getStoredToken();
    if (tok) h['Authorization'] = `Bearer ${tok}`;
    const res = await fetch(`${API_BASE_URL}${path}`, { headers: h });
    if (!res.ok) throw { status: res.status, detail: `CSV download failed: ${res.statusText}`, isApiError: true } as ApiError;
    const blob = await res.blob();
    return URL.createObjectURL(blob);
  },
};
