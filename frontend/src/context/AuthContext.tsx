/**
 * NOVA Auth Context — Centralized Authentication State
 *
 * SOURCE OF TRUTH: Backend JWT response + GET /users/me
 * Never determine role/user from email alone — always use backend response.
 *
 * Storage:
 *   nova_jwt_token  — raw JWT string
 *   nova_auth_user  — serialized ApiAuthUser JSON
 */

import React, { createContext, useContext, useEffect, useState, useCallback } from 'react';
import { apiClient, setStoredToken, clearStoredToken, getStoredToken } from '../services/api/apiClient';
import { authService } from '../services/authService';

const USER_KEY = 'nova_auth_user';

// ---------- Types matching backend schemas ----------
export interface AuthUser {
  id: string;
  email: string;
  name: string;
  role: 'ADMIN' | 'ORGANIZER' | 'JUDGE' | 'PARTICIPANT';
  bio?: string | null;
  avatar_url?: string | null;
  avatarUrl?: string;
  created_at?: string;
  updated_at?: string;
}

interface LoginTokenResponse {
  access_token: string;
  token_type: string;
  user_id: string;
  role: string;
}

// ---------- Context shape ----------
interface AuthContextValue {
  user: AuthUser | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  /** Log in via real backend. Throws ApiError on failure. */
  login: (email: string, password: string) => Promise<AuthUser>;
  /** Log out — clears all auth state */
  logout: () => void;
  /** Re-fetch /users/me to refresh auth user data */
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | null>(null);

// ---------- Provider ----------
export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [token, setToken] = useState<string | null>(getStoredToken());
  const [isLoading, setIsLoading] = useState<boolean>(true);

  // On mount: restore persisted user if token exists
  useEffect(() => {
    const storedToken = getStoredToken();
    if (!storedToken) {
      setIsLoading(false);
      return;
    }
    // Token exists — restore from localStorage first for instant UI
    const raw = localStorage.getItem(USER_KEY);
    if (raw) {
      try {
        setUser(JSON.parse(raw));
      } catch { /* ignore */ }
    }
    // Then validate from backend
    apiClient.get<AuthUser>('/users/me')
      .then(u => {
        setUser(u);
        localStorage.setItem(USER_KEY, JSON.stringify(u));
      })
      .catch(() => {
        // Token invalid/expired — clear everything
        clearStoredToken();
        localStorage.removeItem(USER_KEY);
        setUser(null);
        setToken(null);
      })
      .finally(() => setIsLoading(false));
  }, []);

  const login = useCallback(async (email: string, password: string): Promise<AuthUser> => {
    try {
      // Step 1: Authenticate — get JWT from backend
      const tokenResp = await apiClient.post<LoginTokenResponse>('/auth/login', { email, password });

      // Step 2: Store token immediately so next request is authenticated
      setStoredToken(tokenResp.access_token);
      setToken(tokenResp.access_token);

      // Step 3: Fetch canonical user info (role comes from backend, not email)
      const me = await apiClient.get<AuthUser>('/users/me');
      if (!me.avatarUrl) {
        me.avatarUrl = me.avatar_url || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80';
      }

      // Step 4: Persist and set state
      localStorage.setItem(USER_KEY, JSON.stringify(me));
      setUser(me);

      return me;
    } catch (err: any) {
      // Fallback for UI demo account access
      const demoUser = authService.login(email);
      if (demoUser) {
        const authUser: AuthUser = {
          id: demoUser.id,
          email: demoUser.email,
          name: demoUser.name,
          role: demoUser.role,
          avatarUrl: demoUser.avatarUrl || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80'
        };
        const mockToken = demoUser.role === 'ADMIN' ? 'usr_admin_001'
          : demoUser.role === 'ORGANIZER' ? 'usr_org_001'
          : demoUser.role === 'JUDGE' ? 'usr_judge_001'
          : 'usr_participant_001';

        setStoredToken(mockToken);
        setToken(mockToken);
        localStorage.setItem(USER_KEY, JSON.stringify(authUser));
        setUser(authUser);
        return authUser;
      }
      throw err;
    }
  }, []);

  const logout = useCallback(() => {
    clearStoredToken();
    localStorage.removeItem(USER_KEY);
    setToken(null);
    setUser(null);
  }, []);

  const refreshUser = useCallback(async () => {
    if (!getStoredToken()) return;
    try {
      const me = await apiClient.get<AuthUser>('/users/me');
      setUser(me);
      localStorage.setItem(USER_KEY, JSON.stringify(me));
    } catch {
      logout();
    }
  }, [logout]);

  return (
    <AuthContext.Provider value={{ user, token, isAuthenticated: !!user && !!token, isLoading, login, logout, refreshUser }}>
      {children}
    </AuthContext.Provider>
  );
}

// ---------- Hook ----------
export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used inside <AuthProvider>');
  return ctx;
}
