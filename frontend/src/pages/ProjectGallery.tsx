import React, { useState } from 'react';
import { Submission, Track } from '../mock/types';
import { Grid, ExternalLink, Code2, Eye, ShieldCheck } from 'lucide-react';

interface ProjectGalleryProps {
  submissions: Submission[];
  tracks: Track[];
  searchQuery: string;
}

export const ProjectGallery: React.FC<ProjectGalleryProps> = ({
  submissions,
  tracks,
  searchQuery
}) => {
  const [selectedTrack, setSelectedTrack] = useState<string>('all');
  const [selectedSubmission, setSelectedSubmission] = useState<Submission | null>(null);

  const filteredSubmissions = submissions.filter(s => {
    const matchesTrack = selectedTrack === 'all' || s.trackId === selectedTrack;
    const matchesQuery = searchQuery === '' || 
      s.title.toLowerCase().includes(searchQuery.toLowerCase()) || 
      s.summary.toLowerCase().includes(searchQuery.toLowerCase()) ||
      s.techStack.some(t => t.toLowerCase().includes(searchQuery.toLowerCase()));
    return matchesTrack && matchesQuery;
  });

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* Header Banner */}
      <div className="glass-panel" style={{ padding: '1.75rem', borderRadius: '16px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.375rem' }}>
          <Grid className="w-5 h-5 text-indigo-400" style={{ color: '#818cf8' }} />
          <h1 style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--text-primary)' }}>
            Project Showcase & Gallery
          </h1>
        </div>
        <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
          Explore open-source developer tools, AI agents, and decentralized protocols submitted to NOVA 2026.
        </p>

        {/* Track Filter Pills */}
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', marginTop: '1.25rem' }}>
          <button
            onClick={() => setSelectedTrack('all')}
            className={`btn btn-sm ${selectedTrack === 'all' ? 'btn-primary' : 'btn-secondary'}`}
          >
            All Tracks ({submissions.length})
          </button>
          {tracks.map(t => (
            <button
              key={t.id}
              onClick={() => setSelectedTrack(t.id)}
              className={`btn btn-sm ${selectedTrack === t.id ? 'btn-primary' : 'btn-secondary'}`}
            >
              {t.name}
            </button>
          ))}
        </div>
      </div>

      {/* Projects Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: '1.25rem' }}>
        {filteredSubmissions.map((sub) => (
          <div
            key={sub.id}
            className="glass-panel glass-panel-glow animate-fade-in"
            style={{ padding: '1.25rem', borderRadius: '16px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}
          >
            <div>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
                <span className="badge badge-indigo">{sub.trackName}</span>
                <span className="badge badge-emerald">{sub.status}</span>
              </div>

              <h3 style={{ fontSize: '1.125rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '0.375rem' }}>
                {sub.title}
              </h3>
              <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '0.75rem' }}>
                By {sub.teamName}
              </p>

              <p style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)', lineHeight: 1.5, marginBottom: '1rem', display: '-webkit-box', WebkitLineClamp: 3, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                {sub.summary}
              </p>

              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.375rem', marginBottom: '1.25rem' }}>
                {sub.techStack.map((tech, i) => (
                  <span key={i} className="badge badge-cyan" style={{ fontSize: '0.625rem' }}>
                    {tech}
                  </span>
                ))}
              </div>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', paddingTop: '0.875rem', borderTop: '1px solid var(--border-subtle)' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
                <span>Score: {sub.healthScore}/100</span>
              </div>
              <button onClick={() => setSelectedSubmission(sub)} className="btn btn-secondary btn-sm">
                <Eye className="w-3.5 h-3.5" />
                <span>View Details</span>
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Detail Modal */}
      {selectedSubmission && (
        <div style={{ position: 'fixed', inset: 0, zIndex: 200, background: 'rgba(0,0,0,0.8)', backdropFilter: 'blur(16px)', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '1rem' }}>
          <div className="glass-panel animate-fade-in" style={{ width: '100%', maxWidth: '650px', padding: '2rem', borderRadius: '20px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem' }}>
              <div>
                <span className="badge badge-indigo" style={{ marginBottom: '0.5rem' }}>{selectedSubmission.trackName}</span>
                <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--text-primary)' }}>{selectedSubmission.title}</h2>
                <p style={{ fontSize: '0.8125rem', color: 'var(--text-muted)' }}>Team: {selectedSubmission.teamName}</p>
              </div>
              <button onClick={() => setSelectedSubmission(null)} style={{ background: 'transparent', border: 'none', color: 'var(--text-muted)', fontSize: '1.25rem', cursor: 'pointer' }}>✕</button>
            </div>

            <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', lineHeight: 1.6, marginBottom: '1.5rem' }}>
              {selectedSubmission.description}
            </p>

            <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem', justifyContent: 'flex-end' }}>
              <a href={selectedSubmission.repoUrl} target="_blank" rel="noreferrer" className="btn btn-secondary btn-sm">
                <Code2 className="w-4 h-4" />
                <span>GitHub Repo</span>
              </a>
              <a href={selectedSubmission.demoUrl} target="_blank" rel="noreferrer" className="btn btn-primary btn-sm">
                <ExternalLink className="w-4 h-4" />
                <span>Watch Video Demo</span>
              </a>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
