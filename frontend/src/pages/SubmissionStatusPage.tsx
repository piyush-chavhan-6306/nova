import React from 'react';
import { Submission } from '../mock/types';
import { CheckCircle2, Lock, EyeOff, FileCode, Video, ExternalLink, ShieldCheck, Clock } from 'lucide-react';

interface SubmissionStatusPageProps {
  submission?: Submission;
  onOpenWizard: () => void;
}

export const SubmissionStatusPage: React.FC<SubmissionStatusPageProps> = ({ submission, onOpenWizard }) => {
  if (!submission) {
    return (
      <div className="glass-panel" style={{ padding: '3rem', borderRadius: '20px', textAlign: 'center' }}>
        <h2 style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '0.5rem' }}>
          No Active Submission Found
        </h2>
        <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
          You have not submitted a project for the active hackathon yet.
        </p>
        <button onClick={onOpenWizard} className="btn btn-primary">
          Create Project Submission
        </button>
      </div>
    );
  }

  const steps = [
    { label: 'Draft Created', date: '2026-09-28 14:20', completed: true },
    { label: 'Submitted & Validated', date: '2026-09-28 18:45', completed: true },
    { label: 'Locked for Blind Review', date: '2026-09-28 20:00', completed: submission.status === 'LOCKED' || submission.status === 'SUBMITTED' },
    { label: 'Judge Review In Progress', date: 'Pending', completed: false },
    { label: 'Final Leaderboard Published', date: 'Pending', completed: false }
  ];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* Overview Header */}
      <div className="glass-panel glass-panel-glow" style={{ padding: '2rem', borderRadius: '20px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.375rem' }}>
              <span className="badge badge-emerald">
                <CheckCircle2 className="w-3.5 h-3.5" />
                {submission.status}
              </span>
              <span className="badge badge-indigo">{submission.trackName}</span>
              <span className="badge badge-amber">
                <EyeOff className="w-3.5 h-3.5" />
                Blind Review Protection Active
              </span>
            </div>
            <h1 style={{ fontSize: '2rem', fontWeight: 800, color: 'var(--text-primary)' }}>
              {submission.title}
            </h1>
            <span style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
              Submitted by <strong>{submission.teamName}</strong> • {new Date(submission.submittedAt).toLocaleDateString()}
            </span>
          </div>

          <button onClick={onOpenWizard} className="btn btn-secondary">
            Edit Submission
          </button>
        </div>

        <p style={{ fontSize: '0.9375rem', color: 'var(--text-secondary)', lineHeight: 1.5, maxWidth: '800px' }}>
          {submission.description}
        </p>
      </div>

      {/* Submission Status Timeline */}
      <div className="glass-panel" style={{ padding: '1.5rem', borderRadius: '16px' }}>
        <h3 style={{ fontSize: '1.125rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '1.25rem' }}>
          Submission Progress Lifecycle
        </h3>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
          {steps.map((st, idx) => (
            <div key={idx} style={{
              background: st.completed ? 'rgba(16, 185, 129, 0.08)' : 'rgba(255, 255, 255, 0.02)',
              border: `1px solid ${st.completed ? 'rgba(16, 185, 129, 0.3)' : 'var(--border-subtle)'}`,
              padding: '1rem',
              borderRadius: '12px'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.375rem' }}>
                {st.completed ? (
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                ) : (
                  <Clock className="w-4 h-4 text-slate-500" />
                )}
                <span style={{ fontSize: '0.875rem', fontWeight: 600, color: st.completed ? 'var(--text-primary)' : 'var(--text-muted)' }}>
                  {st.label}
                </span>
              </div>
              <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{st.date}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Technical Assets */}
      <div className="glass-panel" style={{ padding: '1.5rem', borderRadius: '16px' }}>
        <h3 style={{ fontSize: '1.125rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '1rem' }}>
          Submitted Technical Artifacts
        </h3>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          <a href={submission.repoUrl} target="_blank" rel="noreferrer" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0.75rem 1rem', background: 'rgba(255, 255, 255, 0.03)', borderRadius: '10px', textDecoration: 'none', border: '1px solid var(--border-subtle)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--accent-cyan)' }}>
              <FileCode className="w-4 h-4" />
              <span style={{ fontSize: '0.875rem', fontWeight: 600 }}>Source Code Repository</span>
            </div>
            <ExternalLink className="w-4 h-4 text-slate-400" />
          </a>

          <a href={submission.demoUrl} target="_blank" rel="noreferrer" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0.75rem 1rem', background: 'rgba(255, 255, 255, 0.03)', borderRadius: '10px', textDecoration: 'none', border: '1px solid var(--border-subtle)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--accent-indigo)' }}>
              <Video className="w-4 h-4" />
              <span style={{ fontSize: '0.875rem', fontWeight: 600 }}>Video Demonstration</span>
            </div>
            <ExternalLink className="w-4 h-4 text-slate-400" />
          </a>
        </div>
      </div>
    </div>
  );
};
