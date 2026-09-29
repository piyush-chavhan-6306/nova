import React, { useState, useEffect } from 'react';
import { Search, Sparkles, CheckCircle2, Sun, Moon, Lock } from 'lucide-react';
import { Hackathon } from '../mock/types';

interface NavbarProps {
  hackathon: Hackathon;
  searchQuery: string;
  onSearchChange: (q: string) => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  hackathon,
  searchQuery,
  onSearchChange
}) => {
  const [theme, setTheme] = useState<'dark' | 'light'>('dark');

  useEffect(() => {
    document.body.setAttribute('data-theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => prev === 'dark' ? 'light' : 'dark');
  };

  const isClosed = hackathon.status === 'CLOSED';

  return (
    <header style={{
      height: 'var(--navbar-height)',
      background: 'var(--bg-card)',
      borderBottom: '1px solid var(--border-subtle)',
      padding: '0 1.5rem',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      position: 'sticky',
      top: '45px',
      zIndex: 90
    }}>
      {/* Brand & Event Title */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.625rem' }}>
          <div style={{
            width: '36px',
            height: '36px',
            borderRadius: '8px',
            background: 'var(--google-blue)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#fff',
            fontWeight: 700,
            fontSize: '1.25rem',
            boxShadow: '0 2px 6px rgba(26, 115, 232, 0.4)'
          }}>
            N
          </div>
          <div>
            <h1 style={{ fontSize: '1.125rem', fontWeight: 700, color: 'var(--text-primary)', lineHeight: 1.1 }}>
              NOVA
            </h1>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
              Hackathon Portal
            </span>
          </div>
        </div>

      </div>

      {/* Global Search Bar & Actions */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.875rem' }}>
        <div style={{ position: 'relative', width: '280px' }}>
          <Search className="w-4 h-4" style={{
            position: 'absolute',
            left: '0.875rem',
            top: '50%',
            transform: 'translateY(-50%)',
            color: 'var(--text-muted)'
          }} />
          <input
            type="text"
            placeholder="Search projects, tracks, tools..."
            value={searchQuery}
            onChange={(e) => onSearchChange(e.target.value)}
            className="input-field"
            style={{ paddingLeft: '2.5rem', height: '38px', borderRadius: '20px', fontSize: '0.8125rem' }}
          />
        </div>

        {/* Light / Dark Mode Toggle Button */}
        <button
          onClick={toggleTheme}
          className="btn btn-secondary btn-sm"
          style={{ width: '38px', height: '38px', padding: 0, borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}
          title={`Switch to ${theme === 'dark' ? 'Light' : 'Dark'} Mode`}
        >
          {theme === 'dark' ? <Sun className="w-4 h-4 text-amber-400" style={{ color: '#fde293' }} /> : <Moon className="w-4 h-4 text-indigo-600" style={{ color: '#1a73e8' }} />}
        </button>
      </div>
    </header>
  );
};
