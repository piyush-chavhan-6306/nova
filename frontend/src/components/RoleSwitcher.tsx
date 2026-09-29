import React from 'react';
import { UserRole, User } from '../mock/types';
import { Shield, UserCheck, Gavel, Cpu, Code2, LogOut } from 'lucide-react';

interface RoleSwitcherProps {
  currentRole: UserRole;
  currentUser: User;
  onRoleChange: (role: UserRole) => void;
  onLogout: () => void;
}

export const RoleSwitcher: React.FC<RoleSwitcherProps> = ({ currentRole, currentUser, onRoleChange, onLogout }) => {
  const roles: { role: UserRole; label: string; icon: React.ReactNode; color: string }[] = [
    { role: 'PARTICIPANT', label: 'Participant', icon: <Code2 className="w-4 h-4" />, color: '#78d9ec' },
    { role: 'JUDGE', label: 'Judge', icon: <Gavel className="w-4 h-4" />, color: '#fde293' },
    { role: 'ORGANIZER', label: 'Organizer', icon: <UserCheck className="w-4 h-4" />, color: '#81c995' },
    { role: 'ADMIN', label: 'Admin', icon: <Shield className="w-4 h-4" />, color: '#8ab4f8' },
  ];

  return (
    <div style={{
      background: '#202124',
      borderBottom: '1px solid var(--border-subtle)',
      padding: '0.5rem 1.5rem',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      position: 'sticky',
      top: 0,
      zIndex: 100
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
        <span style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)', fontWeight: 600 }}>
          Quick Switch:
        </span>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '0.375rem' }}>
        {roles.map((item) => {
          const isActive = currentRole === item.role;
          return (
            <button
              key={item.role}
              onClick={() => onRoleChange(item.role)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.375rem',
                padding: '0.375rem 0.875rem',
                borderRadius: '16px',
                fontSize: '0.8125rem',
                fontWeight: isActive ? 600 : 500,
                color: isActive ? '#ffffff' : 'var(--text-secondary)',
                background: isActive ? 'rgba(255, 255, 255, 0.1)' : 'transparent',
                border: isActive ? `1px solid ${item.color}` : '1px solid transparent',
                cursor: 'pointer',
                transition: 'all 0.15s ease'
              }}
            >
              <span style={{ color: isActive ? item.color : 'inherit' }}>{item.icon}</span>
              <span>{item.label}</span>
            </button>
          );
        })}
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <img
            src={currentUser.avatarUrl}
            alt={currentUser.name}
            style={{ width: '28px', height: '28px', borderRadius: '50%', objectFit: 'cover', border: '1px solid var(--border-subtle)' }}
          />
          <div style={{ display: 'flex', flexDirection: 'column', textAlign: 'left' }}>
            <span style={{ fontSize: '0.8125rem', fontWeight: 600, color: 'var(--text-primary)' }}>{currentUser.name}</span>
            <span style={{ fontSize: '0.6875rem', color: 'var(--text-muted)' }}>{currentUser.email}</span>
          </div>
        </div>

        <button
          onClick={onLogout}
          className="btn btn-secondary btn-sm"
          title="Logout to Unified Login Screen"
          style={{ padding: '0.25rem 0.625rem', fontSize: '0.75rem' }}
        >
          <LogOut className="w-3.5 h-3.5 text-rose-400" />
          <span>Exit</span>
        </button>
      </div>
    </div>
  );
};
