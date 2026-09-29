import React, { useState } from 'react';
import { Hackathon, User, AuditLogItem } from '../mock/types';
import { Compass, Users, Gavel, Award, ShieldAlert, Settings, Plus, Search, CheckCircle2, Shield, Eye } from 'lucide-react';

// 1. ALL HACKATHONS PAGE
export const AdminHackathonsPage: React.FC<{ hackathons: Hackathon[] }> = ({ hackathons }) => {
  const [filter, setFilter] = useState<string>('ALL');

  const filtered = hackathons.filter(h => {
    if (filter === 'ACTIVE') return h.status === 'ACTIVE';
    if (filter === 'UPCOMING') return h.status === 'UPCOMING';
    if (filter === 'CLOSED') return h.status === 'CLOSED';
    return true;
  });

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      <div className="glass-panel" style={{ padding: '1.75rem', borderRadius: '16px', background: '#292a2d' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.375rem' }}>
          <Compass className="w-5 h-5 text-blue-400" style={{ color: '#8ab4f8' }} />
          <h1 style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--text-primary)' }}>All Platform Hackathons</h1>
        </div>
        <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
          Platform-wide directory of all hackathons across organizers.
        </p>
      </div>

      <div style={{ display: 'flex', gap: '0.5rem' }}>
        {['ALL', 'ACTIVE', 'UPCOMING', 'CLOSED'].map(status => (
          <button
            key={status}
            onClick={() => setFilter(status)}
            className={`btn btn-sm ${filter === status ? 'btn-primary' : 'btn-secondary'}`}
          >
            {status}
          </button>
        ))}
      </div>

      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>Event Name</th>
              <th>Organizer</th>
              <th>Status</th>
              <th>Results State</th>
              <th>Submissions</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map(h => (
              <tr key={h.id}>
                <td style={{ fontWeight: 700, color: 'var(--text-primary)' }}>{h.name}</td>
                <td style={{ color: 'var(--text-secondary)' }}>{h.organizerName || 'Alex Organizer'}</td>
                <td>
                  <span className={`badge ${h.status === 'ACTIVE' ? 'badge-emerald' : h.status === 'UPCOMING' ? 'badge-indigo' : 'badge-amber'}`}>
                    {h.status}
                  </span>
                </td>
                <td><span className="badge badge-cyan">{h.resultsStatus}</span></td>
                <td>{h.submissionCount || 4} Projects</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

// 2. ORGANIZERS MANAGEMENT PAGE
export const AdminOrganizersPage: React.FC<{ users: User[], hackathons: Hackathon[] }> = ({ users, hackathons }) => {
  const organizers = users.filter(u => u.role === 'ORGANIZER');

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      <div className="glass-panel" style={{ padding: '1.75rem', borderRadius: '16px', background: '#292a2d' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.375rem' }}>
          <Users className="w-5 h-5 text-emerald-400" style={{ color: '#81c995' }} />
          <h1 style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--text-primary)' }}>Organizers Roster</h1>
        </div>
        <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
          Multi-tenant isolation and event ownership metrics for registered hackathon organizers.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.25rem' }}>
        {organizers.map(org => (
          <div key={org.id} className="glass-panel" style={{ padding: '1.25rem', borderRadius: '12px', background: '#292a2d' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.875rem', marginBottom: '1rem' }}>
              <img src={org.avatarUrl} alt={org.name} style={{ width: '44px', height: '44px', borderRadius: '50%', border: '1px solid var(--border-subtle)' }} />
              <div>
                <h3 style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-primary)' }}>{org.name}</h3>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{org.email}</span>
              </div>
            </div>
            <div style={{ padding: '0.75rem', background: '#303134', borderRadius: '8px', display: 'flex', justifyContent: 'space-between', fontSize: '0.8125rem' }}>
              <span style={{ color: 'var(--text-muted)' }}>Managed Events:</span>
              <span style={{ fontWeight: 700, color: '#81c995' }}>2 Events Active</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

// 3. JUDGES MANAGEMENT PAGE
export const AdminJudgesPage: React.FC<{ users: User[] }> = ({ users }) => {
  const judges = users.filter(u => u.role === 'JUDGE');

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      <div className="glass-panel" style={{ padding: '1.75rem', borderRadius: '16px', background: '#292a2d' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.375rem' }}>
          <Gavel className="w-5 h-5 text-amber-400" style={{ color: '#fde293' }} />
          <h1 style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--text-primary)' }}>Global Judges Pool</h1>
        </div>
        <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
          Manage global rubric evaluators, workload allocations, and evaluation completion rates.
        </p>
      </div>

      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>Judge Name</th>
              <th>Email</th>
              <th>Role</th>
              <th>Assigned Queue</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {judges.map(j => (
              <tr key={j.id}>
                <td style={{ fontWeight: 700, color: 'var(--text-primary)' }}>{j.name}</td>
                <td>{j.email}</td>
                <td><span className="badge badge-amber">JUDGE</span></td>
                <td>3 Submissions</td>
                <td><span className="badge badge-emerald">ACTIVE</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

// 4. PARTICIPANTS DIRECTORY PAGE
export const AdminParticipantsPage: React.FC<{ users: User[] }> = ({ users }) => {
  const participants = users.filter(u => u.role === 'PARTICIPANT');

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      <div className="glass-panel" style={{ padding: '1.75rem', borderRadius: '16px', background: '#292a2d' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.375rem' }}>
          <Award className="w-5 h-5 text-cyan-400" style={{ color: '#78d9ec' }} />
          <h1 style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--text-primary)' }}>Registered Participants</h1>
        </div>
        <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
          Global roster of hackathon builders and team members across events.
        </p>
      </div>

      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Team Name</th>
              <th>Registration Status</th>
            </tr>
          </thead>
          <tbody>
            {participants.map(p => (
              <tr key={p.id}>
                <td style={{ fontWeight: 700, color: 'var(--text-primary)' }}>{p.name}</td>
                <td>{p.email}</td>
                <td>Quantum Crafters</td>
                <td><span className="badge badge-emerald">REGISTERED</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

// 5. PLATFORM AUDIT TRAIL PAGE
export const AdminAuditPage: React.FC<{ auditLogs: AuditLogItem[] }> = ({ auditLogs }) => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      <div className="glass-panel" style={{ padding: '1.75rem', borderRadius: '16px', background: '#292a2d' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.375rem' }}>
          <ShieldAlert className="w-5 h-5 text-rose-400" style={{ color: '#f28b82' }} />
          <h1 style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--text-primary)' }}>Platform System Audit Logs</h1>
        </div>
        <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
          Immutable audit trail of all role actions, state transitions, and result locks.
        </p>
      </div>

      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>Timestamp</th>
              <th>Actor</th>
              <th>Role</th>
              <th>Action</th>
              <th>Details</th>
            </tr>
          </thead>
          <tbody>
            {auditLogs.map(log => (
              <tr key={log.id}>
                <td style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{log.timestamp}</td>
                <td style={{ fontWeight: 600 }}>{log.actorName}</td>
                <td><span className="badge badge-indigo">{log.actorRole}</span></td>
                <td style={{ fontWeight: 700, color: '#8ab4f8' }}>{log.action}</td>
                <td style={{ color: 'var(--text-secondary)', fontSize: '0.8125rem' }}>{log.details}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

// 6. SYSTEM SETTINGS PAGE
export const AdminSettingsPage: React.FC = () => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      <div className="glass-panel" style={{ padding: '1.75rem', borderRadius: '16px', background: '#292a2d' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.375rem' }}>
          <Settings className="w-5 h-5 text-blue-400" style={{ color: '#8ab4f8' }} />
          <h1 style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--text-primary)' }}>System Settings & Governance</h1>
        </div>
        <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
          Platform feature toggles, security scan policies, and global governance settings.
        </p>
      </div>

      <div className="glass-panel" style={{ padding: '1.5rem', borderRadius: '12px', background: '#292a2d', display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', paddingBottom: '1rem', borderBottom: '1px solid var(--border-subtle)' }}>
          <div>
            <h3 style={{ fontSize: '1rem', fontWeight: 600, color: 'var(--text-primary)' }}>Strict Blind Review Enforcement</h3>
            <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Automatically anonymize team names across all judge workspaces</p>
          </div>
          <span className="badge badge-emerald">ENABLED</span>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', paddingBottom: '1rem', borderBottom: '1px solid var(--border-subtle)' }}>
          <div>
            <h3 style={{ fontSize: '1rem', fontWeight: 600, color: 'var(--text-primary)' }}>Automated CVE Vulnerability Scanning</h3>
            <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Scan GitHub repository dependencies on submission upload</p>
          </div>
          <span className="badge badge-emerald">ACTIVE</span>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div>
            <h3 style={{ fontSize: '1rem', fontWeight: 600, color: 'var(--text-primary)' }}>Multi-Tenant Organizer Scope Lock</h3>
            <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Prevent organizers from modifying events owned by other organizers</p>
          </div>
          <span className="badge badge-indigo">ENFORCED</span>
        </div>
      </div>
    </div>
  );
};
