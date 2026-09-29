import React, { useState } from 'react';
import { PairwiseEvaluation, Submission } from '../mock/types';
import { GitCompare, Trophy, CheckCircle2, ChevronRight, Award } from 'lucide-react';

interface PairwiseJudgingProps {
  evaluations: PairwiseEvaluation[];
  submissions: Submission[];
  onSubmitDecision: (evalId: string, winnerId: string, reason: string) => void;
}

export const PairwiseJudging: React.FC<PairwiseJudgingProps> = ({
  evaluations,
  submissions,
  onSubmitDecision
}) => {
  const activeEval = evaluations[0];
  const [selectedWinner, setSelectedWinner] = useState<string | null>(activeEval?.winnerSubmissionId || null);
  const [reason, setReason] = useState<string>(activeEval?.reason || '');

  const subA = submissions.find(s => s.id === activeEval?.submissionAId);
  const subB = submissions.find(s => s.id === activeEval?.submissionBId);

  const handleSubmit = () => {
    if (activeEval && selectedWinner) {
      onSubmitDecision(activeEval.id, selectedWinner, reason);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* Header Banner */}
      <div className="glass-panel" style={{ padding: '1.75rem', borderRadius: '16px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.375rem' }}>
          <GitCompare className="w-5 h-5 text-indigo-400" style={{ color: '#818cf8' }} />
          <h1 style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--text-primary)' }}>
            Pairwise Head-to-Head Judging
          </h1>
        </div>
        <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
          Compare two assigned project submissions side-by-side and select the stronger entry.
        </p>
      </div>

      {activeEval && subA && subB ? (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          {/* Comparison Cards Grid */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
            {/* Project A Card */}
            <div
              onClick={() => setSelectedWinner(subA.id)}
              className="glass-panel glass-panel-glow"
              style={{
                padding: '1.5rem',
                borderRadius: '16px',
                cursor: 'pointer',
                border: selectedWinner === subA.id ? '2px solid var(--accent-indigo)' : '1px solid var(--border-subtle)',
                background: selectedWinner === subA.id ? 'rgba(99, 102, 241, 0.12)' : 'var(--bg-card)',
                transition: 'all 0.2s ease'
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
                <span className="badge badge-indigo">PROJECT A</span>
                {selectedWinner === subA.id && (
                  <span className="badge badge-emerald">
                    <Trophy className="w-3 h-3" /> WINNER SELECTED
                  </span>
                )}
              </div>

              <h3 style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '0.5rem' }}>
                {subA.title}
              </h3>
              <p style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)', lineHeight: 1.5, marginBottom: '1rem' }}>
                {subA.description}
              </p>

              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.375rem' }}>
                {subA.techStack.map((tech, i) => (
                  <span key={i} className="badge badge-cyan" style={{ fontSize: '0.625rem' }}>
                    {tech}
                  </span>
                ))}
              </div>
            </div>

            {/* Project B Card */}
            <div
              onClick={() => setSelectedWinner(subB.id)}
              className="glass-panel glass-panel-glow"
              style={{
                padding: '1.5rem',
                borderRadius: '16px',
                cursor: 'pointer',
                border: selectedWinner === subB.id ? '2px solid var(--accent-indigo)' : '1px solid var(--border-subtle)',
                background: selectedWinner === subB.id ? 'rgba(99, 102, 241, 0.12)' : 'var(--bg-card)',
                transition: 'all 0.2s ease'
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
                <span className="badge badge-indigo">PROJECT B</span>
                {selectedWinner === subB.id && (
                  <span className="badge badge-emerald">
                    <Trophy className="w-3 h-3" /> WINNER SELECTED
                  </span>
                )}
              </div>

              <h3 style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '0.5rem' }}>
                {subB.title}
              </h3>
              <p style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)', lineHeight: 1.5, marginBottom: '1rem' }}>
                {subB.description}
              </p>

              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.375rem' }}>
                {subB.techStack.map((tech, i) => (
                  <span key={i} className="badge badge-cyan" style={{ fontSize: '0.625rem' }}>
                    {tech}
                  </span>
                ))}
              </div>
            </div>
          </div>

          {/* Decision Reason & Submit Box */}
          <div className="glass-panel" style={{ padding: '1.5rem', borderRadius: '16px' }}>
            <div className="input-group">
              <label className="input-label">Decision Justification / Reason *</label>
              <textarea
                rows={3}
                placeholder="Explain why the selected entry demonstrated superior architecture, UI/UX, or technical execution..."
                value={reason}
                onChange={(e) => setReason(e.target.value)}
                className="input-field"
              />
            </div>

            <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '1rem' }}>
              <button
                onClick={handleSubmit}
                disabled={!selectedWinner}
                className="btn btn-primary btn-sm"
                style={{ opacity: !selectedWinner ? 0.4 : 1 }}
              >
                <Award className="w-4 h-4" />
                <span>Submit Pairwise Decision</span>
              </button>
            </div>
          </div>
        </div>
      ) : (
        <div className="glass-panel" style={{ padding: '2rem', textAlign: 'center' }}>
          <p style={{ color: 'var(--text-muted)' }}>No pairwise comparison tasks pending.</p>
        </div>
      )}
    </div>
  );
};
