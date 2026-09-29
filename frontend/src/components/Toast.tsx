import React, { useEffect } from 'react';
import { CheckCircle2, AlertTriangle, XCircle, Info } from 'lucide-react';

export interface ToastMessage {
  id: string;
  type: 'success' | 'warning' | 'error' | 'info';
  message: string;
}

interface ToastProps {
  toasts: ToastMessage[];
  onDismiss: (id: string) => void;
}

export const Toast: React.FC<ToastProps> = ({ toasts, onDismiss }) => {
  return (
    <div style={{
      position: 'fixed',
      bottom: '1.5rem',
      right: '1.5rem',
      zIndex: 300,
      display: 'flex',
      flexDirection: 'column',
      gap: '0.5rem'
    }}>
      {toasts.map((t) => (
        <div
          key={t.id}
          className="glass-panel animate-fade-in"
          style={{
            padding: '0.75rem 1.25rem',
            borderRadius: '12px',
            display: 'flex',
            alignItems: 'center',
            gap: '0.75rem',
            background: t.type === 'success' ? 'rgba(16, 185, 129, 0.15)' : t.type === 'warning' ? 'rgba(245, 158, 11, 0.15)' : 'rgba(99, 102, 241, 0.15)',
            border: t.type === 'success' ? '1px solid rgba(16, 185, 129, 0.3)' : '1px solid rgba(245, 158, 11, 0.3)',
            boxShadow: '0 8px 32px rgba(0,0,0,0.5)',
            fontSize: '0.875rem',
            color: 'var(--text-primary)'
          }}
        >
          {t.type === 'success' && <CheckCircle2 className="w-4 h-4 text-emerald-400" />}
          {t.type === 'warning' && <AlertTriangle className="w-4 h-4 text-amber-400" />}
          {t.type === 'info' && <Info className="w-4 h-4 text-indigo-400" />}
          <span>{t.message}</span>
          <button onClick={() => onDismiss(t.id)} style={{ background: 'transparent', border: 'none', color: 'var(--text-muted)', cursor: 'pointer', marginLeft: '0.5rem' }}>✕</button>
        </div>
      ))}
    </div>
  );
};
