import React, { useState } from 'react';
import { UserRole } from '../mock/types';
import { DEMO_ACCOUNTS } from '../mock/users';
import { Shield, UserCheck, Gavel, Code2, ArrowRight, Lock, AlertCircle, Loader2 } from 'lucide-react';
import { useAuth, AuthUser } from '../context/AuthContext';

/** Password seeded for all demo accounts in the FastAPI backend via seed_demo_users.py */
const DEMO_PASSWORD = 'nova2026!';

interface LoginPageProps {
  /** Called with backend-authenticated user after successful login */
  onLoginSuccess: (user: AuthUser) => void;
}

export const LoginPage: React.FC<LoginPageProps> = ({ onLoginSuccess }) => {
  const { login } = useAuth();
  const [email, setEmail] = useState<string>('participant@nova.dev');
  const [password, setPassword] = useState<string>(DEMO_PASSWORD);
  const [loading, setLoading] = useState<boolean>(false);
  const [loadingEmail, setLoadingEmail] = useState<string>('');
  const [error, setError] = useState<string>('');

  // --- Normal form submit: uses whatever email+password the user typed ---
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    setLoadingEmail(email);
    try {
      // login() calls POST /auth/login then GET /users/me
      // Role comes from backend — NOT from the email string
      const user = await login(email, password);
      onLoginSuccess(user);
    } catch (err: any) {
      setError(
        err?.detail ||
        err?.message ||
        'Login failed. Please check your credentials and ensure the backend is running.'
      );
    } finally {
      setLoading(false);
      setLoadingEmail('');
    }
  };

  // --- Quick demo login: same real backend, preset email + demo password ---
  const handleQuickLogin = async (demoEmail: string) => {
    if (loading) return;
    setError('');
    setEmail(demoEmail);
    setPassword(DEMO_PASSWORD);
    setLoading(true);
    setLoadingEmail(demoEmail);
    try {
      // Same code path as normal login — no role bypass
      const user = await login(demoEmail, DEMO_PASSWORD);
      onLoginSuccess(user);
    } catch (err: any) {
      setError(
        err?.detail ||
        err?.message ||
        `Login failed for ${demoEmail}. Ensure the FastAPI backend is running at http://localhost:8000 and demo credentials are seeded.`
      );
    } finally {
      setLoading(false);
      setLoadingEmail('');
    }
  };

  const demoCards: Array<{
    role: UserRole;
    email: string;
    name: string;
    avatarUrl: string;
    badgeColor: string;
    Icon: React.ElementType;
  }> = [
    { role: 'ADMIN', email: 'admin@nova.dev', name: DEMO_ACCOUNTS.ADMIN.name, avatarUrl: DEMO_ACCOUNTS.ADMIN.avatarUrl || '', badgeColor: 'badge-indigo', Icon: Shield },
    { role: 'ORGANIZER', email: 'organizer@nova.dev', name: DEMO_ACCOUNTS.ORGANIZER.name, avatarUrl: DEMO_ACCOUNTS.ORGANIZER.avatarUrl || '', badgeColor: 'badge-emerald', Icon: UserCheck },
    { role: 'JUDGE', email: 'judge@nova.dev', name: DEMO_ACCOUNTS.JUDGE.name, avatarUrl: DEMO_ACCOUNTS.JUDGE.avatarUrl || '', badgeColor: 'badge-amber', Icon: Gavel },
    { role: 'PARTICIPANT', email: 'participant@nova.dev', name: DEMO_ACCOUNTS.PARTICIPANT.name, avatarUrl: DEMO_ACCOUNTS.PARTICIPANT.avatarUrl || '', badgeColor: 'badge-cyan', Icon: Code2 },
  ];

  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '2rem', background: '#202124' }}>
      <div style={{ width: '100%', maxWidth: '900px' }}>

        {/* Branding Header */}
        <div style={{ textAlign: 'center', marginBottom: '2.5rem' }}>
          <div style={{
            display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
            width: '56px', height: '56px', borderRadius: '16px',
            background: 'var(--google-blue)', color: '#fff', fontWeight: 700,
            fontSize: '1.75rem', marginBottom: '1rem',
            boxShadow: '0 4px 12px rgba(26, 115, 232, 0.4)'
          }}>
            N
          </div>
          <h1 style={{ fontSize: '2.25rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '0.5rem' }}>
            NOVA Hackathon Portal
          </h1>
          <p style={{ fontSize: '0.9375rem', color: 'var(--text-secondary)' }}>
            Sign in with your account credentials or use a demo role below.
          </p>
        </div>

        {/* Error Banner */}
        {error && (
          <div style={{
            display: 'flex', alignItems: 'flex-start', gap: '0.625rem',
            padding: '0.875rem 1rem',
            background: 'rgba(234,67,53,0.12)', border: '1px solid rgba(234,67,53,0.35)',
            borderRadius: '10px', marginBottom: '1.25rem'
          }}>
            <AlertCircle className="w-4 h-4" style={{ color: '#ea4335', flexShrink: 0, marginTop: '2px' }} />
            <span style={{ fontSize: '0.875rem', color: '#ea4335', lineHeight: 1.5 }}>{error}</span>
          </div>
        )}

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))', gap: '2rem' }}>

          {/* ── Left: Email/Password Form ── */}
          <div className="glass-panel" style={{ padding: '2rem', borderRadius: '16px', background: '#292a2d' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1.5rem' }}>
              <Lock className="w-4 h-4" style={{ color: 'var(--google-blue)' }} />
              <h2 style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--text-primary)' }}>Account Sign In</h2>
            </div>

            <form onSubmit={handleSubmit}>
              <div className="input-group">
                <label className="input-label">Email Address</label>
                <input
                  id="login-email"
                  type="email"
                  value={email}
                  onChange={e => setEmail(e.target.value)}
                  placeholder="e.g. participant@nova.dev"
                  className="input-field"
                  autoComplete="email"
                  required
                  disabled={loading}
                />
              </div>

              <div className="input-group" style={{ marginBottom: '1.5rem' }}>
                <label className="input-label">Password</label>
                <input
                  id="login-password"
                  type="password"
                  value={password}
                  onChange={e => setPassword(e.target.value)}
                  placeholder="Enter password"
                  className="input-field"
                  autoComplete="current-password"
                  required
                  disabled={loading}
                />
              </div>

              <button
                id="login-submit-btn"
                type="submit"
                className="btn btn-primary"
                style={{ width: '100%', padding: '0.75rem 1rem' }}
                disabled={loading}
              >
                {loading && loadingEmail === email ? (
                  <span style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', justifyContent: 'center' }}>
                    <Loader2 className="w-4 h-4" style={{ animation: 'spin 0.8s linear infinite' }} />
                    Authenticating…
                  </span>
                ) : (
                  <>
                    <span>Sign In & Continue</span>
                    <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </button>
            </form>

            <div style={{ marginTop: '1.5rem', paddingTop: '1rem', borderTop: '1px solid var(--border-subtle)', textAlign: 'center' }}>
              <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '0.25rem' }}>Demo password for all accounts:</p>
              <code style={{ fontSize: '0.8125rem', color: 'var(--google-blue)', fontFamily: 'monospace', letterSpacing: '0.05em' }}>
                nova2026!
              </code>
            </div>
          </div>

          {/* ── Right: Quick Demo Cards ── */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <h3 style={{ fontSize: '0.8125rem', fontWeight: 700, color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.06em' }}>
              Quick Demo Account Access
            </h3>
            <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '-0.5rem', marginBottom: '0.25rem' }}>
              Each button authenticates through the real FastAPI backend.
            </p>

            {demoCards.map(card => {
              const isThisLoading = loading && loadingEmail === card.email;
              return (
                <button
                  key={card.role}
                  id={`quick-login-${card.role.toLowerCase()}`}
                  onClick={() => handleQuickLogin(card.email)}
                  disabled={loading}
                  className="glass-panel"
                  style={{
                    width: '100%', padding: '1rem 1.25rem', borderRadius: '12px',
                    background: '#292a2d', cursor: loading ? 'not-allowed' : 'pointer',
                    display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                    border: isThisLoading ? '1px solid var(--google-blue)' : undefined,
                    opacity: loading && !isThisLoading ? 0.55 : 1,
                    transition: 'opacity 0.2s, border 0.2s',
                    textAlign: 'left',
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.875rem' }}>
                    <img
                      src={card.avatarUrl}
                      alt={card.name}
                      style={{ width: '40px', height: '40px', borderRadius: '50%', objectFit: 'cover', border: '1px solid var(--border-subtle)' }}
                    />
                    <div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.125rem' }}>
                        <span style={{ fontSize: '0.9375rem', fontWeight: 700, color: 'var(--text-primary)' }}>{card.name}</span>
                        <span className={`badge ${card.badgeColor}`}>{card.role}</span>
                      </div>
                      <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{card.email}</span>
                    </div>
                  </div>

                  <div className="btn btn-secondary btn-sm" style={{ pointerEvents: 'none', minWidth: '88px', justifyContent: 'center' }}>
                    {isThisLoading ? (
                      <span style={{ display: 'flex', alignItems: 'center', gap: '0.375rem' }}>
                        <Loader2 className="w-3 h-3" style={{ animation: 'spin 0.8s linear infinite' }} />
                        <span>Logging in</span>
                      </span>
                    ) : (
                      'Log in →'
                    )}
                  </div>
                </button>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
};
