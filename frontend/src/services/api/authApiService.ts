import { apiClient, TOKEN_STORAGE_KEY, USER_STORAGE_KEY } from './apiClient';

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user_id: string;
  role: string;
}

export interface ApiUser {
  id: string;
  email: string;
  name: string;
  role: string;
  bio?: string | null;
  avatar_url?: string | null;
  created_at: string;
  updated_at: string;
}

export const authApiService = {
  async login(email: string, password: string): Promise<{ token: LoginResponse; user: ApiUser }> {
    const token = await apiClient.post<LoginResponse>('/auth/login', { email, password });
    localStorage.setItem(TOKEN_STORAGE_KEY, token.access_token);
    const user = await apiClient.get<ApiUser>('/users/me');
    localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(user));
    return { token, user };
  },

  async getMe(): Promise<ApiUser | null> {
    try {
      const user = await apiClient.get<ApiUser>('/users/me');
      localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(user));
      return user;
    } catch {
      return null;
    }
  },

  logout(): void {
    localStorage.removeItem(TOKEN_STORAGE_KEY);
    localStorage.removeItem(USER_STORAGE_KEY);
  },

  getSavedUser(): ApiUser | null {
    const raw = localStorage.getItem(USER_STORAGE_KEY);
    if (!raw) return null;
    try { return JSON.parse(raw); } catch { return null; }
  },

  isAuthenticated(): boolean {
    return !!localStorage.getItem(TOKEN_STORAGE_KEY);
  },
};
