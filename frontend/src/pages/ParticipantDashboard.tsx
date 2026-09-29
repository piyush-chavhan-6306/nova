import React from 'react';
import { Submission, Team } from '../mock/types';
import { Send, Users, Sparkles, CheckCircle2, ShieldAlert, ArrowRight, ExternalLink } from 'lucide-react';

interface ParticipantDashboardProps {
  submissions: Submission[];
  team?: Team;
  onOpenWizard: () => void;
}

export const ParticipantDashboard: React.FC<ParticipantDashboardProps> = ({
  submissions,
  team,
  onOpenWizard
}) => {
  const activeSub = submissions[0];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* Welcome Hero Card */}
      <div className="glass-panel glass-panel-glow" style={{ padding: '2rem', borderRadius: '20px', position: 'relative', overflow: 'hidden' }}>
        <div style={{ position: 'relative', zIndex: 2 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
            <span className="badge badge-indigo">
              <Sparkles className="w-3 h-3" />
              Participant Studio
            </span>
            <span className="badge badge-emerald">Team Active</span>
          </div>
          <h1 style={{ fontSize: '2rem', fontWeight: 800, color: 'var(--text-primary)', marginBottom: '0.5rem' }}>
            Welcome back, Priya!
          </h1>
          <p style={{ fontSize: '0.9375rem', color: 'var(--text-secondary)', maxWidth: '600px', lineHeight: 1.5 }}>
            Manage your project submission for <strong>NOVA 2026</strong>. Submit technical repositories, media demos, and review your team status.
          </p>
          <div style={{ marginTop: '1.25rem', display: 'flex', gap: '0.75rem' }}>
            <button onClick={onOpenWizard} className="btn btn-primary">
              <Send className="w-4 h-4" />
              <span>{activeSub ? 'Edit Project Submission' : 'Create New Submission'}</span>
            </button>
          </div>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '1rem' }}>
        <div className="glass-panel" style={{ padding: '1.25rem' }}>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', fontWeight: 600 }}>Active Team</span>
          <div style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--text-primary)', marginTop: '0.25rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Users className="w-5 h-5 text-indigo-400" style={{ color: '#818cf8' }} />
            {team ? team.name : 'No Active Team'}
          </div>
          <span style={{ fontSize: '0.75rem', color: 'var(--accent-emerald)', marginTop: '0.375rem', display: 'block' }}>
            {team ? `${team.members.length} Verified Members` : 'Create or Join a team to submit'}
          </span>
        </div>

        <div className="glass-panel" style={{ padding: '1.25rem' }}>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', fontWeight: 600 }}>Submission Status</span>
          <div style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--text-primary)', marginTop: '0.25rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <CheckCircle2 className="w-5 h-5" style={{ color: '#34d399' }} />
            {activeSub?.status || 'SUBMITTED'}
          </div>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.375rem', display: 'block' }}>
            Locked for Blind Review
          </span>
        </div>


      </div>

      {/* Active Project Card */}
      {activeSub && (
        <div className="glass-panel" style={{ padding: '1.5rem', borderRadius: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
              <h3 style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                {activeSub.title}
              </h3>
              <span className="badge badge-indigo">{activeSub.trackName}</span>
            </div>
            <button onClick={onOpenWizard} className="btn btn-secondary btn-sm">
              Manage
            </button>
          </div>

          <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', marginBottom: '1.25rem', lineHeight: 1.5 }}>
            {activeSub.description}
          </p>

          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', marginBottom: '1.25rem' }}>
            {activeSub.techStack.map((tech, i) => (
              <span key={i} className="badge badge-cyan" style={{ fontSize: '0.6875rem' }}>
                {tech}
              </span>
            ))}
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', paddingTop: '1rem', borderTop: '1px solid var(--border-subtle)' }}>
            <a href={activeSub.repoUrl} target="_blank" rel="noreferrer" style={{ fontSize: '0.8125rem', color: 'var(--accent-cyan)', display: 'flex', alignItems: 'center', gap: '0.25rem', textDecoration: 'none' }}>
              <span>GitHub Repository</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </a>
            <a href={activeSub.demoUrl} target="_blank" rel="noreferrer" style={{ fontSize: '0.8125rem', color: 'var(--accent-indigo)', display: 'flex', alignItems: 'center', gap: '0.25rem', textDecoration: 'none' }}>
              <span>Demo Video</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </a>
          </div>
        </div>
      )}
    </div>
  );
};
