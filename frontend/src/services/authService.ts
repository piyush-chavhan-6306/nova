import { User, UserRole } from '../mock/types';
import { DEMO_ACCOUNTS } from '../mock/users';

const AUTH_STORAGE_KEY = 'nova_demo_auth_user';

export class AuthService {
  private currentUser: User | null = null;

  constructor() {
    const saved = localStorage.getItem(AUTH_STORAGE_KEY);
    if (saved) {
      try {
        this.currentUser = JSON.parse(saved);
      } catch {
        this.currentUser = DEMO_ACCOUNTS.PARTICIPANT;
      }
    } else {
      this.currentUser = DEMO_ACCOUNTS.PARTICIPANT;
    }
  }

  getCurrentUser(): User | null {
    return this.currentUser;
  }

  login(email: string): User | null {
    const cleanEmail = email.trim().toLowerCase();
    
    let matchedUser: User | null = null;
    if (cleanEmail === 'admin@nova.dev') matchedUser = DEMO_ACCOUNTS.ADMIN;
    else if (cleanEmail === 'organizer@nova.dev') matchedUser = DEMO_ACCOUNTS.ORGANIZER;
    else if (cleanEmail === 'judge@nova.dev') matchedUser = DEMO_ACCOUNTS.JUDGE;
    else if (cleanEmail === 'participant@nova.dev') matchedUser = DEMO_ACCOUNTS.PARTICIPANT;
    else {
      // Fallback match based on substring role keyword
      if (cleanEmail.includes('admin')) matchedUser = DEMO_ACCOUNTS.ADMIN;
      else if (cleanEmail.includes('org')) matchedUser = DEMO_ACCOUNTS.ORGANIZER;
      else if (cleanEmail.includes('judge')) matchedUser = DEMO_ACCOUNTS.JUDGE;
      else matchedUser = DEMO_ACCOUNTS.PARTICIPANT;
    }

    this.currentUser = matchedUser;
    localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(matchedUser));
    return matchedUser;
  }

  switchRole(role: UserRole): User {
    const user = DEMO_ACCOUNTS[role] || DEMO_ACCOUNTS.PARTICIPANT;
    this.currentUser = user;
    localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(user));
    return user;
  }

  logout(): void {
    this.currentUser = null;
    localStorage.removeItem(AUTH_STORAGE_KEY);
  }

  getRedirectForRole(role: UserRole): string {
    switch (role) {
      case 'ADMIN': return '/admin/dashboard';
      case 'ORGANIZER': return '/organizer/dashboard';
      case 'JUDGE': return '/judge/dashboard';
      case 'PARTICIPANT': return '/participant/dashboard';
      default: return '/participant/dashboard';
    }
  }
}

export const authService = new AuthService();
