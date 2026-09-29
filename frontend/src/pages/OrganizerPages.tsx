import React from 'react';
import { Hackathon, Submission, LeaderboardResult, AuditLogItem, IntegrityAlert } from '../mock/types';
import { UserCheck, Users, Send, Gavel, Sliders, Trophy, Download, ShieldAlert, CheckCircle2, Lock, FileSpreadsheet } from 'lucide-react';

// 1. PARTICIPANTS MANAGEMENT
export const OrganizerParticipantsPage: React.FC<{ hackathon: Hackathon }> = ({ hackathon }) => (
  <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
    <div className="glass-panel" style={{ padding: '1.75rem', borderRadius: '16px', background: '#292a2d' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.375rem' }}>
        <UserCheck className="w-5 h-5 text-emerald-400" style={{ color: '#81c995' }} />
        <h1 style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--text-primary)' }}>{hackathon.name} — Registered Participants</h1>
      </div>
      <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
        Manage participant rosters, verify team assignments, and issue invitations.
      </p>
    </div>

    <div className="table-container">
      <table className="data-table">
        <thead>
          <tr>
            <th>Participant Name</th>
            <th>Email</th>
            <th>Team Name</th>
            <th>Role</th>
            <th>Verification</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td style={{ fontWeight: 700 }}>Priya Sharma</td>
            <td>participant@nova.dev</td>
            <td>Quantum Crafters</td>
            <td><span className="badge badge-indigo">CAPTAIN</span></td>
            <td><span className="badge badge-emerald">VERIFIED</span></td>
          </tr>
          <tr>
            <td style={{ fontWeight: 700 }}>Alex Chen</td>
            <td>alex.chen@nova.dev</td>
            <td>Quantum Crafters</td>
            <td><span className="badge badge-cyan">MEMBER</span></td>
            <td><span className="badge badge-emerald">VERIFIED</span></td>
          </tr>
          <tr>
            <td style={{ fontWeight: 700 }}>Sara Miller</td>
            <td>sara.m@nova.dev</td>
            <td>CyberForge Labs</td>
            <td><span className="badge badge-indigo">CAPTAIN</span></td>
            <td><span className="badge badge-emerald">VERIFIED</span></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
);

// 2. TEAMS MANAGEMENT
export const OrganizerTeamsPage: React.FC = () => (
  <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
    <div className="glass-panel" style={{ padding: '1.75rem', borderRadius: '16px', background: '#292a2d' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.375rem' }}>
        <Users className="w-5 h-5 text-blue-400" style={{ color: '#8ab4f8' }} />
        <h1 style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--text-primary)' }}>Event Teams Directory</h1>
      </div>
      <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
        Registered builder teams, invite code status, and member rosters.
      </p>
    </div>

    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.25rem' }}>
      {[
        { name: 'Quantum Crafters', members: 3, code: 'QC-2026-X9', project: 'Quiet Hours' },
        { name: 'CyberForge Labs', members: 4, code: 'CF-8821-K2', project: 'Glass Signal' },
        { name: 'Zero Knowledge Guild', members: 2, code: 'ZK-9912-P4', project: 'Deep Compass' }
      ].map((t, i) => (
        <div key={i} className="glass-panel" style={{ padding: '1.25rem', borderRadius: '12px', background: '#292a2d' }}>
          <h3 style={{ fontSize: '1.125rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '0.375rem' }}>{t.name}</h3>
          <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '0.75rem' }}>Invite Code: {t.code}</p>
          <div style={{ padding: '0.625rem', background: '#303134', borderRadius: '8px', fontSize: '0.8125rem' }}>
            <span style={{ color: 'var(--text-secondary)' }}>Project: </span>
            <span style={{ fontWeight: 600, color: '#8ab4f8' }}>{t.project}</span>
          </div>
        </div>
      ))}
    </div>
  </div>
);

// 3. SUBMISSIONS MANAGEMENT
export const OrganizerSubmissionsPage: React.FC<{ submissions: Submission[] }> = ({ submissions }) => (
  <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
    <div className="glass-panel" style={{ padding: '1.75rem', borderRadius: '16px', background: '#292a2d' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.375rem' }}>
        <Send className="w-5 h-5 text-indigo-400" style={{ color: '#8ab4f8' }} />
        <h1 style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--text-primary)' }}>Submissions Management</h1>
      </div>
      <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
        Monitor project submission locks, blind review states, and repository links.
      </p>
    </div>

    <div className="table-container">
      <table className="data-table">
        <thead>
          <tr>
            <th>Title</th>
            <th>Track</th>
            <th>Team</th>
            <th>Status</th>
            <th>Submitted At</th>
          </tr>
        </thead>
        <tbody>
          {submissions.map(s => (
            <tr key={s.id}>
              <td style={{ fontWeight: 700, color: 'var(--text-primary)' }}>{s.title}</td>
              <td><span className="badge badge-indigo">{s.trackName}</span></td>
              <td style={{ color: 'var(--text-secondary)' }}>{s.teamName}</td>
              <td><span className="badge badge-emerald">{s.status}</span></td>
              <td style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{new Date(s.submittedAt).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  </div>
);

// 4. JUDGES & WORKLOADS
export const OrganizerJudgesPage: React.FC = () => (
  <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
    <div className="glass-panel" style={{ padding: '1.75rem', borderRadius: '16px', background: '#292a2d' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.375rem' }}>
        <Gavel className="w-5 h-5 text-amber-400" style={{ color: '#fde293' }} />
        <h1 style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--text-primary)' }}>Judges & Workload Distribution</h1>
      </div>
      <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
        Assign submission review queues and balance judge workload across tracks.
      </p>
    </div>

    <div className="table-container">
      <table className="data-table">
        <thead>
          <tr>
            <th>Judge Name</th>
            <th>Email</th>
            <th>Assigned Queue</th>
            <th>Completed Reviews</th>
            <th>Progress</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td style={{ fontWeight: 700 }}>Dr. Ada Okonkwo</td>
            <td>judge@nova.dev</td>
            <td>3 Submissions</td>
            <td>1 / 3</td>
            <td><span className="badge badge-amber">33% Done</span></td>
          </tr>
          <tr>
            <td style={{ fontWeight: 700 }}>Prof. Marcus Vance</td>
            <td>marcus.v@nova.dev</td>
            <td>3 Submissions</td>
            <td>3 / 3</td>
            <td><span className="badge badge-emerald">100% Done</span></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
);

// 5. RUBRIC CONFIG
export const OrganizerRubricPage: React.FC<{ hackathon: Hackathon }> = ({ hackathon }) => (
  <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
    <div className="glass-panel" style={{ padding: '1.75rem', borderRadius: '16px', background: '#292a2d' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.375rem' }}>
        <Sliders className="w-5 h-5 text-indigo-400" style={{ color: '#8ab4f8' }} />
        <h1 style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--text-primary)' }}>Evaluation Rubric Configuration</h1>
      </div>
      <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
        Configure evaluation criteria, maximum points, and weighted scoring formulas.
      </p>
    </div>

    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
      {hackathon.rubric.map(r => (
        <div key={r.id} className="glass-panel" style={{ padding: '1.25rem', borderRadius: '12px', background: '#292a2d', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h3 style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '0.25rem' }}>{r.name}</h3>
            <p style={{ fontSize: '0.8125rem', color: 'var(--text-muted)' }}>{r.description}</p>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <span className="badge badge-indigo">Max Score: {r.maxScore}</span>
            <span className="badge badge-emerald">Weight: {r.weight}x</span>
          </div>
        </div>
      ))}
    </div>
  </div>
);

// 6. RESULTS & LIFECYCLE
export const OrganizerResultsPage: React.FC<{ leaderboard: LeaderboardResult[], hackathon: Hackathon, onUpdateResultsStatus: (s: Hackathon['resultsStatus']) => void }> = ({ leaderboard, hackathon, onUpdateResultsStatus }) => (
  <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
    <div className="glass-panel" style={{ padding: '1.75rem', borderRadius: '16px', background: '#292a2d' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.375rem' }}>
        <Trophy className="w-5 h-5 text-amber-400" style={{ color: '#fde293' }} />
        <h1 style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--text-primary)' }}>Leaderboard & Finite State Machine</h1>
      </div>
      <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
        Calibrated scoring leaderboard and results publication state controls.
      </p>
    </div>

    <div className="table-container">
      <table className="data-table">
        <thead>
          <tr>
            <th>Rank</th>
            <th>Project Title</th>
            <th>Team Name</th>
            <th>Track</th>
            <th>Raw Score</th>
            <th>Calibrated Score</th>
          </tr>
        </thead>
        <tbody>
          {leaderboard.map(lb => (
            <tr key={lb.submissionId}>
              <td style={{ fontWeight: 800, color: '#fde293' }}>#{lb.rank}</td>
              <td style={{ fontWeight: 700 }}>{lb.projectTitle}</td>
              <td>{lb.teamName}</td>
              <td><span className="badge badge-indigo">{lb.trackName}</span></td>
              <td>{lb.rawScore.toFixed(2)}</td>
              <td style={{ fontWeight: 700, color: '#81c995' }}>{lb.calibratedScore.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  </div>
);

// 7. CSV EXPORTS PAGE
export const OrganizerExportsPage: React.FC<{ onExportCSV: (type: string) => void }> = ({ onExportCSV }) => (
  <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
    <div className="glass-panel" style={{ padding: '1.75rem', borderRadius: '16px', background: '#292a2d' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.375rem' }}>
        <Download className="w-5 h-5 text-blue-400" style={{ color: '#8ab4f8' }} />
        <h1 style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--text-primary)' }}>CSV Export Center</h1>
      </div>
      <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
        Export official hackathon results, judge evaluation sheets, and audit logs.
      </p>
    </div>

    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '1.25rem' }}>
      {[
        { type: 'results', label: 'Export Leaderboard CSV', desc: 'Calibrated ranks and final scores' },
        { type: 'reviews', label: 'Export Judge Scores CSV', desc: 'Raw rubric scores & comments' },
        { type: 'audit', label: 'Export Audit Logs CSV', desc: 'Event activity trail' }
      ].map(exp => (
        <div key={exp.type} className="glass-panel" style={{ padding: '1.5rem', borderRadius: '12px', background: '#292a2d' }}>
          <FileSpreadsheet className="w-8 h-8 text-blue-400" style={{ color: '#8ab4f8', marginBottom: '0.75rem' }} />
          <h3 style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '0.25rem' }}>{exp.label}</h3>
          <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '1rem' }}>{exp.desc}</p>
          <button onClick={() => onExportCSV(exp.type)} className="btn btn-primary btn-sm">
            <Download className="w-4 h-4" /> Download CSV
          </button>
        </div>
      ))}
    </div>
  </div>
);

// 8. AUDIT LOGS PAGE
export const OrganizerAuditPage: React.FC<{ auditLogs: AuditLogItem[], alerts: IntegrityAlert[] }> = ({ auditLogs, alerts }) => (
  <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
    <div className="glass-panel" style={{ padding: '1.75rem', borderRadius: '16px', background: '#292a2d' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.375rem' }}>
        <ShieldAlert className="w-5 h-5 text-rose-400" style={{ color: '#f28b82' }} />
        <h1 style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--text-primary)' }}>Event Audit Trail & Integrity Alerts</h1>
      </div>
      <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
        Real-time audit log of judge submissions and outlier detection alerts.
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
          {auditLogs.map(l => (
            <tr key={l.id}>
              <td style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{l.timestamp}</td>
              <td style={{ fontWeight: 600 }}>{l.actorName}</td>
              <td><span className="badge badge-indigo">{l.actorRole}</span></td>
              <td style={{ fontWeight: 700, color: '#8ab4f8' }}>{l.action}</td>
              <td style={{ color: 'var(--text-secondary)', fontSize: '0.8125rem' }}>{l.details}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  </div>
);
