import React from 'react';
import { Hackathon, User, AuditLogItem } from '../mock/types';
import { Server, Compass, Users, Gavel, BarChart3, ShieldCheck, Activity } from 'lucide-react';

interface AdminDashboardProps {
  stats: {
    totalHackathons: number;
    activeHackathons: number;
    totalParticipants: number;
    totalOrganizers: number;
    totalJudges: number;
    totalSubmissions: number;
  };
  hackathons: Hackathon[];
  users: User[];
  auditLogs: AuditLogItem[];
}

export const AdminDashboard: React.FC<AdminDashboardProps> = ({
  stats,
  hackathons,
  users,
  auditLogs
}) => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* Platform Banner */}
      <div className="glass-panel glass-panel-glow" style={{ padding: '2rem', borderRadius: '20px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
          <Server className="w-5 h-5 text-indigo-400" />
          <span style={{ fontSize: '0.8125rem', fontWeight: 700, color: '#818cf8', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            PLATFORM ROOT ADMINISTRATOR
          </span>
        </div>
        <h1 style={{ fontSize: '2rem', fontWeight: 800, color: 'var(--text-primary)', marginBottom: '0.5rem' }}>
          Platform Executive Dashboard
        </h1>
        <p style={{ fontSize: '0.9375rem', color: 'var(--text-secondary)', maxWidth: '750px' }}>
          Platform-wide oversight spanning across all hackathons, organizers, judges, participants, and system audit logs.
        </p>
      </div>

      {/* Metric Cards Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1.25rem' }}>
        <div className="glass-panel" style={{ padding: '1.25rem' }}>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', fontWeight: 600 }}>Total Hackathons</span>
          <div style={{ fontSize: '1.75rem', fontWeight: 800, color: 'var(--text-primary)', marginTop: '0.25rem' }}>
            {stats.totalHackathons} Events
          </div>
          <span style={{ fontSize: '0.75rem', color: 'var(--accent-emerald)', marginTop: '0.25rem', display: 'block' }}>
            {stats.activeHackathons} Currently Active
          </span>
        </div>

        <div className="glass-panel" style={{ padding: '1.25rem' }}>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', fontWeight: 600 }}>Platform Participants</span>
          <div style={{ fontSize: '1.75rem', fontWeight: 800, color: '#38bdf8', marginTop: '0.25rem' }}>
            {stats.totalParticipants}
          </div>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.25rem', display: 'block' }}>
            Across all active events
          </span>
        </div>

        <div className="glass-panel" style={{ padding: '1.25rem' }}>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', fontWeight: 600 }}>Registered Organizers</span>
          <div style={{ fontSize: '1.75rem', fontWeight: 800, color: '#34d399', marginTop: '0.25rem' }}>
            {stats.totalOrganizers}
          </div>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.25rem', display: 'block' }}>
            Multi-Tenant Isolated
          </span>
        </div>

        <div className="glass-panel" style={{ padding: '1.25rem' }}>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', fontWeight: 600 }}>Global Judges</span>
          <div style={{ fontSize: '1.75rem', fontWeight: 800, color: '#fbbf24', marginTop: '0.25rem' }}>
            {stats.totalJudges}
          </div>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.25rem', display: 'block' }}>
            Rubric Evaluators
          </span>
        </div>
      </div>

      {/* Platform Hackathons Table & System Logs */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '1.5rem' }}>
        <div className="glass-panel" style={{ padding: '1.5rem', borderRadius: '16px' }}>
          <h3 style={{ fontSize: '1.125rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '1rem' }}>
            All Platform Hackathons
          </h3>

          <div className="table-container">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Event Name</th>
                  <th>Organizer</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {hackathons.map((h) => (
                  <tr key={h.id}>
                    <td style={{ fontWeight: 700 }}>{h.name}</td>
                    <td style={{ color: 'var(--text-secondary)' }}>{h.organizerName || 'Alex Organizer'}</td>
                    <td><span className="badge badge-emerald">{h.status}</span></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="glass-panel" style={{ padding: '1.5rem', borderRadius: '16px' }}>
          <h3 style={{ fontSize: '1.125rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '1rem' }}>
            Platform System Audit Feed
          </h3>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            {auditLogs.slice(0, 5).map((log) => (
              <div key={log.id} style={{ padding: '0.75rem 1rem', borderRadius: '10px', background: 'rgba(255, 255, 255, 0.02)', border: '1px solid var(--border-subtle)' }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.25rem' }}>
                  <span style={{ fontSize: '0.8125rem', fontWeight: 700, color: 'var(--text-primary)' }}>{log.action}</span>
                  <span className="badge badge-indigo">{log.actorRole}</span>
                </div>
                <p style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>{log.details}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
