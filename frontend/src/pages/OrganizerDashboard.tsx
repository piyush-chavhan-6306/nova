import React, { useState } from 'react';
import { Hackathon, LeaderboardResult, AuditLogItem, IntegrityAlert, Submission } from '../mock/types';
import {
  BarChart3, EyeOff, ShieldCheck, Download, Trophy, Users, AlertTriangle,
  Lock, CheckCircle2, RefreshCw, FileSpreadsheet
} from 'lucide-react';

interface OrganizerDashboardProps {
  hackathon: Hackathon;
  submissions: Submission[];
  leaderboard: LeaderboardResult[];
  auditLogs: AuditLogItem[];
  alerts: IntegrityAlert[];
  onToggleBlindReview: () => void;
  onUpdateResultsStatus: (status: Hackathon['resultsStatus']) => void;
  onExportCSV: (type: string) => void;
}

export const OrganizerDashboard: React.FC<OrganizerDashboardProps> = ({
  hackathon,
  submissions,
  leaderboard,
  auditLogs,
  alerts,
  onToggleBlindReview,
  onUpdateResultsStatus,
  onExportCSV
}) => {
  const [activeTab, setActiveTab] = useState<'overview' | 'leaderboard' | 'audit'>('overview');

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* Executive Header Banner */}
      <div className="glass-panel glass-panel-glow" style={{ padding: '1.75rem', borderRadius: '16px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.375rem' }}>
              <BarChart3 className="w-5 h-5 text-emerald-400" style={{ color: '#34d399' }} />
              <h1 style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--text-primary)' }}>
                Organizer Executive Command Center
              </h1>
            </div>
            <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
              Manage hackathon lifecycle, judge calibration, blind review mode, result locks, and audit trails.
            </p>
          </div>

          <div style={{ display: 'flex', gap: '0.75rem' }}>
            <button onClick={() => onExportCSV('results')} className="btn btn-secondary btn-sm">
              <FileSpreadsheet className="w-4 h-4 text-emerald-400" />
              <span>Export CSV</span>
            </button>
          </div>
        </div>
      </div>

      {/* KPI Metrics Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1rem' }}>
        <div className="glass-panel" style={{ padding: '1.25rem' }}>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', fontWeight: 600 }}>Total Projects</span>
          <div style={{ fontSize: '1.75rem', fontWeight: 800, color: 'var(--text-primary)', marginTop: '0.25rem' }}>
            {submissions.length} Submissions
          </div>
          <span style={{ fontSize: '0.75rem', color: 'var(--accent-emerald)' }}>100% Verified</span>
        </div>

        <div className="glass-panel" style={{ padding: '1.25rem' }}>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', fontWeight: 600 }}>Result State Machine</span>
          <div style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--accent-indigo)', marginTop: '0.375rem' }}>
            <span className="badge badge-indigo" style={{ fontSize: '0.875rem' }}>{hackathon.resultsStatus}</span>
          </div>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.25rem', display: 'block' }}>
            Finite Lifecycle Controlled
          </span>
        </div>

        <div className="glass-panel" style={{ padding: '1.25rem' }}>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', fontWeight: 600 }}>Integrity Alerts</span>
          <div style={{ fontSize: '1.75rem', fontWeight: 800, color: '#fbbf24', marginTop: '0.25rem' }}>
            {alerts.length} Flagged
          </div>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Score Outlier Mitigation</span>
        </div>
      </div>

      {/* Sub-Navigation Tabs */}
      <div style={{ display: 'flex', gap: '0.5rem', borderBottom: '1px solid var(--border-subtle)', paddingBottom: '0.5rem' }}>
        <button
          onClick={() => setActiveTab('overview')}
          className={`btn btn-sm ${activeTab === 'overview' ? 'btn-primary' : 'btn-secondary'}`}
        >
          Executive Overview
        </button>
        <button
          onClick={() => setActiveTab('leaderboard')}
          className={`btn btn-sm ${activeTab === 'leaderboard' ? 'btn-primary' : 'btn-secondary'}`}
        >
          Results & Leaderboard
        </button>
        <button
          onClick={() => setActiveTab('audit')}
          className={`btn btn-sm ${activeTab === 'audit' ? 'btn-primary' : 'btn-secondary'}`}
        >
          Audit Logs & Alerts ({auditLogs.length})
        </button>
      </div>

      {/* Tab 1: Executive Overview */}
      {activeTab === 'overview' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          {/* Result Lifecycle Controls */}
          <div className="glass-panel" style={{ padding: '1.5rem', borderRadius: '16px' }}>
            <h3 style={{ fontSize: '1.125rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '0.5rem' }}>
              Result Lifecycle Finite State Machine
            </h3>
            <p style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)', marginBottom: '1.25rem' }}>
              Transition official hackathon evaluation results through required compliance stages.
            </p>

            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.75rem' }}>
              {['DRAFT', 'CALCULATED', 'UNDER_REVIEW', 'APPROVED', 'PUBLISHED', 'LOCKED'].map((st) => {
                const isActive = hackathon.resultsStatus === st;
                return (
                  <button
                    key={st}
                    onClick={() => onUpdateResultsStatus(st as any)}
                    className={`btn btn-sm ${isActive ? 'btn-primary' : 'btn-secondary'}`}
                    style={{
                      border: isActive ? '1px solid var(--accent-indigo)' : '1px solid var(--border-subtle)'
                    }}
                  >
                    {isActive && <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />}
                    <span>{st}</span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Integrity Alert Section */}
          <div className="glass-panel" style={{ padding: '1.5rem', borderRadius: '16px' }}>
            <h3 style={{ fontSize: '1.125rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '1rem' }}>
              System Integrity & Outlier Audit Alerts
            </h3>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              {alerts.map((alt) => (
                <div key={alt.id} style={{
                  padding: '1rem',
                  borderRadius: '10px',
                  background: alt.severity === 'HIGH' ? 'rgba(244, 63, 94, 0.1)' : 'rgba(245, 158, 11, 0.1)',
                  border: alt.severity === 'HIGH' ? '1px solid rgba(244, 63, 94, 0.3)' : '1px solid rgba(245, 158, 11, 0.3)',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.75rem'
                }}>
                  <AlertTriangle className="w-4 h-4 text-amber-400" />
                  <div style={{ flex: 1 }}>
                    <div style={{ fontSize: '0.8125rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                      [{alt.severity}] {alt.type}
                    </div>
                    <p style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginTop: '0.125rem' }}>
                      {alt.message}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Tab 2: Leaderboard */}
      {activeTab === 'leaderboard' && (
        <div className="glass-panel" style={{ padding: '1.5rem', borderRadius: '16px' }}>
          <h3 style={{ fontSize: '1.125rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '1rem' }}>
            Calibrated Score & Pairwise Leaderboard
          </h3>

          <div className="table-container">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Rank</th>
                  <th>Project Title</th>
                  <th>Team</th>
                  <th>Track</th>
                  <th>Raw Score</th>
                  <th>Calibrated Score</th>
                  <th>Pairwise Win %</th>
                </tr>
              </thead>
              <tbody>
                {leaderboard.map((lb) => (
                  <tr key={lb.rank}>
                    <td>
                      <span className="badge badge-indigo">#{lb.rank}</span>
                    </td>
                    <td style={{ fontWeight: 700 }}>{lb.projectTitle}</td>
                    <td style={{ color: 'var(--text-secondary)' }}>{lb.teamName}</td>
                    <td><span className="badge badge-cyan">{lb.trackName}</span></td>
                    <td>{lb.rawScore} / 10</td>
                    <td style={{ fontWeight: 700, color: '#34d399' }}>{lb.calibratedScore} / 10</td>
                    <td style={{ color: '#38bdf8', fontWeight: 700 }}>{lb.pairwiseWinRate}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Tab 3: Audit Logs */}
      {activeTab === 'audit' && (
        <div className="glass-panel" style={{ padding: '1.5rem', borderRadius: '16px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <h3 style={{ fontSize: '1.125rem', fontWeight: 700, color: 'var(--text-primary)' }}>
              System Action Audit Logs
            </h3>
            <button onClick={() => onExportCSV('audit')} className="btn btn-secondary btn-sm">
              <Download className="w-3.5 h-3.5" />
              <span>Export Log CSV</span>
            </button>
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
                {auditLogs.map((log) => (
                  <tr key={log.id}>
                    <td style={{ fontSize: '0.75rem', fontFamily: 'monospace', color: 'var(--text-muted)' }}>
                      {new Date(log.timestamp).toLocaleTimeString()}
                    </td>
                    <td style={{ fontWeight: 600 }}>{log.actorName}</td>
                    <td><span className="badge badge-indigo">{log.actorRole}</span></td>
                    <td style={{ fontWeight: 600, color: '#38bdf8' }}>{log.action}</td>
                    <td style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)' }}>{log.details}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};
