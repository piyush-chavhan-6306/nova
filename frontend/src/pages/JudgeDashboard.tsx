import React, { useState } from 'react';
import { JudgeAssignment, Submission, Review, Hackathon } from '../mock/types';
import {
  Gavel, CheckCircle2, Clock, EyeOff, Star, Save, Send, AlertTriangle,
  FolderGit2, Video, ExternalLink, ShieldCheck, Cpu, Code2, Play
} from 'lucide-react';

interface JudgeDashboardProps {
  assignments: JudgeAssignment[];
  submissions: Submission[];
  hackathon: Hackathon;
  onSaveReview: (submissionId: string, scores: any[], comment: string, isSubmit: boolean) => void;
}

export const JudgeDashboard: React.FC<JudgeDashboardProps> = ({
  assignments,
  submissions,
  hackathon,
  onSaveReview
}) => {
  const [activeSubmissionId, setActiveSubmissionId] = useState<string | null>(null);
  const [scores, setScores] = useState<Record<string, number>>({
    rub_01: 9,
    rub_02: 8,
    rub_03: 9,
    rub_04: 8
  });
  const [comment, setComment] = useState<string>('Impressive architecture and production readiness.');
  const [isVideoPlaying, setIsVideoPlaying] = useState<boolean>(false);

  const selectedSubmission = submissions.find(s => s.id === activeSubmissionId);

  const handleOpenEvaluation = (submissionId: string) => {
    setActiveSubmissionId(submissionId);
    setIsVideoPlaying(false);
  };

  const handleScoreChange = (rubricId: string, val: number) => {
    setScores(prev => ({ ...prev, [rubricId]: val }));
  };

  const handleSave = (isSubmit: boolean) => {
    if (activeSubmissionId) {
      const formattedScores = hackathon.rubric.map(r => ({
        criterionId: r.id,
        criterionName: r.name,
        score: scores[r.id] || 8
      }));
      onSaveReview(activeSubmissionId, formattedScores, comment, isSubmit);
      setActiveSubmissionId(null);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* Header Banner */}
      <div className="glass-panel" style={{ padding: '1.75rem', borderRadius: '16px', background: '#292a2d' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.375rem' }}>
              <Gavel className="w-5 h-5 text-amber-400" style={{ color: '#fde293' }} />
              <h1 style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                Judge Evaluation Workspace
              </h1>
            </div>
            <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
              Evaluate assigned projects according to official track rubrics, source repositories, and video demos.
            </p>
          </div>

          {hackathon.blindReviewEnabled && (
            <span className="badge badge-amber">
              <EyeOff className="w-3.5 h-3.5" />
              Blind Review Active (Teams Anonymized)
            </span>
          )}
        </div>
      </div>

      {/* Assignment Queue List */}
      <div className="glass-panel" style={{ padding: '1.5rem', borderRadius: '16px', background: '#292a2d' }}>
        <h3 style={{ fontSize: '1.125rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '1rem' }}>
          Assigned Projects Queue ({assignments.length})
        </h3>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.875rem' }}>
          {assignments.map((asg) => {
            const sub = submissions.find(s => s.id === asg.submissionId);
            const isCompleted = asg.status === 'COMPLETED';

            return (
              <div
                key={asg.id}
                className="glass-panel animate-fade-in"
                style={{
                  padding: '1.25rem',
                  borderRadius: '12px',
                  background: '#303134',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  borderLeft: isCompleted ? '4px solid var(--google-green)' : '4px solid var(--google-yellow)'
                }}
              >
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
                    <span style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                      {asg.submissionTitle}
                    </span>
                    <span className="badge badge-indigo">{asg.trackName}</span>
                  </div>
                  <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                    Team: {hackathon.blindReviewEnabled ? 'Anonymous Team (Blind Review)' : sub?.teamName}
                  </p>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                  {isCompleted ? (
                    <span className="badge badge-emerald">
                      <CheckCircle2 className="w-3.5 h-3.5" /> Evaluated
                    </span>
                  ) : (
                    <span className="badge badge-amber">
                      <Clock className="w-3.5 h-3.5" /> Pending Review
                    </span>
                  )}

                  <button
                    onClick={() => handleOpenEvaluation(asg.submissionId)}
                    className={`btn btn-sm ${isCompleted ? 'btn-secondary' : 'btn-primary'}`}
                  >
                    <span>{isCompleted ? 'Edit Review' : 'Start Review'}</span>
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Rubric Evaluation Modal with Repo & Video Inspection */}
      {selectedSubmission && (
        <div style={{ position: 'fixed', inset: 0, zIndex: 200, background: 'rgba(0,0,0,0.85)', backdropFilter: 'blur(16px)', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '1.5rem' }}>
          <div className="glass-panel animate-fade-in" style={{ width: '100%', maxWidth: '850px', maxHeight: '90vh', overflowY: 'auto', padding: '2rem', borderRadius: '20px', background: '#202124', border: '1px solid #3c4043' }}>

            {/* Modal Header */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1.25rem', paddingBottom: '1rem', borderBottom: '1px solid var(--border-subtle)' }}>
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.375rem' }}>
                  <span className="badge badge-indigo">{selectedSubmission.trackName}</span>
                  {selectedSubmission.cveScanStatus === 'PASSED' && (
                    <span className="badge badge-emerald">
                      <ShieldCheck className="w-3.5 h-3.5" /> Security Scan Passed
                    </span>
                  )}
                </div>
                <h2 style={{ fontSize: '1.75rem', fontWeight: 700, color: 'var(--text-primary)' }}>{selectedSubmission.title}</h2>
                <p style={{ fontSize: '0.8125rem', color: 'var(--text-muted)' }}>
                  Author: {hackathon.blindReviewEnabled ? 'ANONYMOUS TEAM (Blind Review Enabled)' : selectedSubmission.teamName}
                </p>
              </div>
              <button onClick={() => setActiveSubmissionId(null)} style={{ background: '#303134', border: '1px solid #5f6368', color: 'var(--text-primary)', width: '32px', height: '32px', borderRadius: '50%', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1rem' }}>✕</button>
            </div>

            {/* Summary & Description */}
            <div className="glass-panel" style={{ padding: '1.25rem', borderRadius: '12px', marginBottom: '1.5rem', background: '#292a2d' }}>
              <h4 style={{ fontSize: '0.875rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '0.375rem' }}>
                Project Overview
              </h4>
              <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', lineHeight: 1.6, marginBottom: '0.875rem' }}>
                {selectedSubmission.description}
              </p>

              {/* Tech Stack Chips */}
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.375rem' }}>
                {selectedSubmission.techStack.map((tech, i) => (
                  <span key={i} className="badge badge-cyan" style={{ fontSize: '0.75rem' }}>
                    {tech}
                  </span>
                ))}
              </div>
            </div>

            {/* CRITICAL: SUBMISSION RESOURCES & EVALUATION MEDIA (Repo & Video) */}
            <div className="glass-panel" style={{ padding: '1.25rem', borderRadius: '12px', marginBottom: '1.5rem', background: 'rgba(26, 115, 232, 0.08)', border: '1px solid rgba(138, 180, 248, 0.3)' }}>
              <h4 style={{ fontSize: '0.9375rem', fontWeight: 700, color: '#8ab4f8', marginBottom: '0.875rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <Code2 className="w-4 h-4" />
                Submission Materials & Verification Artifacts
              </h4>

              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '1rem', marginBottom: '1rem' }}>
                {/* GitHub Repository Action Button */}
                <a
                  href={selectedSubmission.repoUrl}
                  target="_blank"
                  rel="noreferrer"
                  className="btn btn-primary"
                  style={{ justifyContent: 'space-between', padding: '0.75rem 1rem', background: '#303134', border: '1px solid #5f6368', color: '#e8eaed' }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <FolderGit2 className="w-4 h-4 text-blue-400" style={{ color: '#8ab4f8' }} />
                    <span>GitHub Repository</span>
                  </div>
                  <ExternalLink className="w-4 h-4" style={{ color: 'var(--text-muted)' }} />
                </a>

                {/* Demo Video Action Button */}
                <a
                  href={selectedSubmission.demoUrl}
                  target="_blank"
                  rel="noreferrer"
                  className="btn btn-primary"
                  style={{ justifyContent: 'space-between', padding: '0.75rem 1rem', background: 'var(--google-blue)' }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <Video className="w-4 h-4" />
                    <span>Watch Demo Video</span>
                  </div>
                  <ExternalLink className="w-4 h-4" />
                </a>
              </div>

              {/* Interactive Demo Video Player Preview Box */}
              <div style={{
                background: '#171717',
                borderRadius: '12px',
                border: '1px solid #3c4043',
                padding: '1.25rem',
                textAlign: 'center',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '0.75rem',
                minHeight: '180px'
              }}>
                {isVideoPlaying ? (
                  <div style={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.5rem' }}>
                    <div style={{ padding: '0.5rem', background: 'rgba(30, 142, 62, 0.2)', border: '1px solid #81c995', borderRadius: '8px', color: '#81c995', fontSize: '0.8125rem' }}>
                      ▶ Simulating Demo Video Stream for {selectedSubmission.title}
                    </div>
                    <video
                      controls
                      autoPlay
                      style={{ width: '100%', maxHeight: '220px', borderRadius: '8px', background: '#000' }}
                      src="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4"
                    />
                  </div>
                ) : (
                  <>
                    <div style={{ width: '48px', height: '48px', borderRadius: '50%', background: 'rgba(138, 180, 248, 0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#8ab4f8', cursor: 'pointer' }} onClick={() => setIsVideoPlaying(true)}>
                      <Play className="w-6 h-6 ml-0.5" />
                    </div>
                    <div>
                      <h5 style={{ fontSize: '0.9375rem', fontWeight: 600, color: 'var(--text-primary)' }}>
                        Embedded Technical Walkthrough Preview
                      </h5>
                      <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                        Click play to watch demo video directly inside Judge Evaluation Workspace
                      </span>
                    </div>
                    <button onClick={() => setIsVideoPlaying(true)} className="btn btn-secondary btn-sm" style={{ marginTop: '0.25rem' }}>
                      <Play className="w-3.5 h-3.5" />
                      <span>Play Walkthrough</span>
                    </button>
                  </>
                )}
              </div>

            </div>

            {/* Rubric Criteria Sliders */}
            <h3 style={{ fontSize: '1.125rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '1rem' }}>
              Official Rubric Criteria Evaluation
            </h3>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem', marginBottom: '1.5rem' }}>
              {hackathon.rubric.map((r) => (
                <div key={r.id} className="glass-panel" style={{ padding: '1rem', borderRadius: '12px', background: '#292a2d' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.375rem' }}>
                    <span style={{ fontWeight: 600, fontSize: '0.875rem', color: 'var(--text-primary)' }}>{r.name}</span>
                    <span style={{ fontSize: '0.875rem', fontWeight: 700, color: '#8ab4f8' }}>
                      {scores[r.id] || 8} / {r.maxScore}
                    </span>
                  </div>
                  <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '0.75rem' }}>{r.description}</p>

                  <input
                    type="range"
                    min="1"
                    max={r.maxScore}
                    step="0.5"
                    value={scores[r.id] || 8}
                    onChange={(e) => handleScoreChange(r.id, parseFloat(e.target.value))}
                    style={{ width: '100%', accentColor: 'var(--google-blue)', cursor: 'pointer' }}
                  />
                </div>
              ))}
            </div>

            {/* Comments */}
            <div className="input-group">
              <label className="input-label">Judge Qualitative Technical Feedback & Comments</label>
              <textarea
                rows={3}
                placeholder="Provide detailed technical feedback on the codebase, architecture, and video demo..."
                value={comment}
                onChange={(e) => setComment(e.target.value)}
                className="input-field"
                style={{ background: '#292a2d' }}
              />
            </div>

            {/* Actions */}
            <div style={{ display: 'flex', gap: '1rem', marginTop: '1.5rem', justifyContent: 'flex-end' }}>
              <button onClick={() => handleSave(false)} className="btn btn-secondary btn-sm">
                <Save className="w-4 h-4" />
                <span>Save Draft</span>
              </button>
              <button onClick={() => handleSave(true)} className="btn btn-primary btn-sm">
                <Send className="w-4 h-4" />
                <span>Submit & Lock Evaluation</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
