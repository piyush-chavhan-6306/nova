import React, { useState } from 'react';
import { User, UserRole } from '../mock/types';
import { Users, Search, Shield, UserCheck, Gavel, Code2 } from 'lucide-react';

interface AdminUsersPageProps {
  users: User[];
}

export const AdminUsersPage: React.FC<AdminUsersPageProps> = ({ users }) => {
  const [roleFilter, setRoleFilter] = useState<string>('ALL');
  const [search, setSearch] = useState<string>('');

  const filteredUsers = users.filter(u => {
    if (roleFilter !== 'ALL' && u.role !== roleFilter) return false;
    if (search && !u.name.toLowerCase().includes(search.toLowerCase()) && !u.email.toLowerCase().includes(search.toLowerCase())) return false;
    return true;
  });

  const getRoleBadge = (role: UserRole) => {
    switch (role) {
      case 'ADMIN': return <span className="badge badge-indigo"><Shield className="w-3.5 h-3.5" /> ADMIN</span>;
      case 'ORGANIZER': return <span className="badge badge-emerald"><UserCheck className="w-3.5 h-3.5" /> ORGANIZER</span>;
      case 'JUDGE': return <span className="badge badge-amber"><Gavel className="w-3.5 h-3.5" /> JUDGE</span>;
      case 'PARTICIPANT': return <span className="badge badge-cyan"><Code2 className="w-3.5 h-3.5" /> PARTICIPANT</span>;
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      <div className="glass-panel glass-panel-glow" style={{ padding: '2rem', borderRadius: '20px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
          <Users className="w-5 h-5 text-indigo-400" />
          <span style={{ fontSize: '0.8125rem', fontWeight: 700, color: '#818cf8', textTransform: 'uppercase' }}>
            PLATFORM USER DIRECTORY
          </span>
        </div>
        <h1 style={{ fontSize: '2rem', fontWeight: 800, color: 'var(--text-primary)' }}>
          All Platform Users ({users.length})
        </h1>
        <p style={{ fontSize: '0.9375rem', color: 'var(--text-secondary)' }}>
          Manage global user accounts across ADMIN, ORGANIZER, JUDGE, and PARTICIPANT roles.
        </p>
      </div>

      <div style={{ display: 'flex', flexWrap: 'wrap', alignItems: 'center', justifyContent: 'space-between', gap: '1rem' }}>
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          {['ALL', 'ADMIN', 'ORGANIZER', 'JUDGE', 'PARTICIPANT'].map(role => (
            <button
              key={role}
              onClick={() => setRoleFilter(role)}
              className={`btn btn-sm ${roleFilter === role ? 'btn-primary' : 'btn-secondary'}`}
            >
              {role}
            </button>
          ))}
        </div>

        <div style={{ position: 'relative', width: '280px' }}>
          <Search className="w-4 h-4" style={{ position: 'absolute', left: '0.75rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
          <input
            type="text"
            placeholder="Search users by name or email..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="input-field"
            style={{ paddingLeft: '2.25rem', height: '36px' }}
          />
        </div>
      </div>

      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>User</th>
              <th>Email</th>
              <th>System Role</th>
              <th>User ID</th>
              <th>Bio / Title</th>
            </tr>
          </thead>
          <tbody>
            {filteredUsers.map((u) => (
              <tr key={u.id}>
                <td>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                    <img src={u.avatarUrl || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150'} alt={u.name} style={{ width: '36px', height: '36px', borderRadius: '50%', objectFit: 'cover' }} />
                    <span style={{ fontWeight: 700, color: 'var(--text-primary)' }}>{u.name}</span>
                  </div>
                </td>
                <td style={{ color: 'var(--text-secondary)' }}>{u.email}</td>
                <td>{getRoleBadge(u.role)}</td>
                <td style={{ fontFamily: 'monospace', fontSize: '0.75rem', color: 'var(--text-muted)' }}>{u.id}</td>
                <td style={{ fontSize: '0.8125rem', color: 'var(--text-muted)' }}>{u.bio || 'Platform User'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
