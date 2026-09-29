import React, { useState } from 'react';
import { Submission } from '../mock/types';
import { CheckCircle2, ChevronRight, ChevronLeft, ShieldCheck, Code, Video, FileText, AlertTriangle } from 'lucide-react';

interface SubmissionWizardProps {
  initialSubmission?: Submission;
  onSave: (submission: Partial<Submission>) => void;
  onClose: () => void;
}

export const SubmissionWizard: React.FC<SubmissionWizardProps> = ({
  initialSubmission,
  onSave,
  onClose
}) => {
  const [step, setStep] = useState<number>(1);
  const [title, setTitle] = useState(initialSubmission?.title || '');
  const [summary, setSummary] = useState(initialSubmission?.summary || '');
  const [description, setDescription] = useState(initialSubmission?.description || '');
  const [trackId, setTrackId] = useState(initialSubmission?.trackId || 'trk_01');
  const [repoUrl, setRepoUrl] = useState(initialSubmission?.repoUrl || '');
  const [demoUrl, setDemoUrl] = useState(initialSubmission?.demoUrl || '');
  const [techStackInput, setTechStackInput] = useState(initialSubmission?.techStack.join(', ') || 'React, TypeScript, Python, FastAPI');

  const handleNext = () => {
    if (step < 4) setStep(step + 1);
  };

  const handleBack = () => {
    if (step > 1) setStep(step - 1);
  };

  const handleSubmit = () => {
    const techStack = techStackInput.split(',').map(s => s.trim()).filter(Boolean);
    onSave({
      id: initialSubmission?.id,
      title,
      summary,
      description,
      trackId,
      trackName: trackId === 'trk_01' ? 'Developer Tools & Automation' : trackId === 'trk_02' ? 'Artificial Intelligence & Agents' : 'Web3 & Decentralized Infrastructure',
      repoUrl,
      demoUrl,
      techStack,
      status: 'SUBMITTED'
    });
    onClose();
  };

  return (
    <div style={{
      position: 'fixed',
      inset: 0,
      zIndex: 200,
      background: 'rgba(0, 0, 0, 0.8)',
      backdropFilter: 'blur(16px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '1.5rem'
    }}>
      <div className="glass-panel animate-fade-in" style={{
        width: '100%',
        maxWidth: '750px',
        maxHeight: '90vh',
        overflowY: 'auto',
        padding: '2rem',
        borderRadius: '20px',
        border: '1px solid var(--border-glow)'
      }}>
        {/* Wizard Stepper Header */}
        <div style={{ marginBottom: '1.5rem', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div>
            <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--text-primary)' }}>
              Project Submission Studio
            </h2>
            <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
              Configure technical details, repositories, and media demos for evaluation.
            </p>
          </div>
          <button onClick={onClose} style={{ background: 'transparent', border: 'none', color: 'var(--text-muted)', fontSize: '1.25rem', cursor: 'pointer' }}>✕</button>
        </div>

        {/* Step Progress Bar */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '0.5rem', marginBottom: '2rem' }}>
          {[
            { id: 1, label: '1. Overview', icon: <FileText className="w-3.5 h-3.5" /> },
            { id: 2, label: '2. Repos & Tech', icon: <Code className="w-3.5 h-3.5" /> },
            { id: 3, label: '3. Media Demo', icon: <Video className="w-3.5 h-3.5" /> },
            { id: 4, label: '4. Pre-Flight Lock', icon: <ShieldCheck className="w-3.5 h-3.5" /> },
          ].map((s) => {
            const isActive = step === s.id;
            const isDone = step > s.id;
            return (
              <div
                key={s.id}
                style={{
                  padding: '0.5rem',
                  borderRadius: '8px',
                  background: isActive ? 'var(--gradient-primary)' : isDone ? 'rgba(16, 185, 129, 0.2)' : 'rgba(255, 255, 255, 0.04)',
                  color: isActive || isDone ? '#ffffff' : 'var(--text-muted)',
                  fontSize: '0.75rem',
                  fontWeight: 600,
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.375rem',
                  transition: 'all 0.2s ease'
                }}
              >
                {isDone ? <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" /> : s.icon}
                <span>{s.label}</span>
              </div>
            );
          })}
        </div>

        {/* Step Content */}
        {step === 1 && (
          <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div className="input-group">
              <label className="input-label">Project Title *</label>
              <input
                type="text"
                placeholder="e.g. Quiet Hours"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="input-field"
              />
            </div>

            <div className="input-group">
              <label className="input-label">Target Hackathon Track *</label>
              <select
                value={trackId}
                onChange={(e) => setTrackId(e.target.value)}
                className="input-field"
              >
                <option value="trk_01">Developer Tools & Automation</option>
                <option value="trk_02">Artificial Intelligence & Agents</option>
                <option value="trk_03">Web3 & Decentralized Infrastructure</option>
              </select>
            </div>

            <div className="input-group">
              <label className="input-label">Short Summary (Elevator Pitch) *</label>
              <input
                type="text"
                placeholder="One line summary describing your project's main innovation"
                value={summary}
                onChange={(e) => setSummary(e.target.value)}
                className="input-field"
              />
            </div>

            <div className="input-group">
              <label className="input-label">Full Technical Description *</label>
              <textarea
                rows={4}
                placeholder="Detailed breakdown of architecture, design decisions, and algorithms..."
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                className="input-field"
                style={{ resize: 'vertical' }}
              />
            </div>
          </div>
        )}

        {step === 2 && (
          <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div className="input-group">
              <label className="input-label">GitHub Repository URL *</label>
              <input
                type="url"
                placeholder="https://github.com/org/repository"
                value={repoUrl}
                onChange={(e) => setRepoUrl(e.target.value)}
                className="input-field"
              />
            </div>

            <div className="input-group">
              <label className="input-label">Tech Stack (comma separated) *</label>
              <input
                type="text"
                placeholder="React, TypeScript, Python, FastAPI, PostgreSQL"
                value={techStackInput}
                onChange={(e) => setTechStackInput(e.target.value)}
                className="input-field"
              />
            </div>

            {/* Mock Unsupported Feature Component Showcase */}
            <div className="glass-panel" style={{ padding: '1rem', borderRadius: '12px', background: 'rgba(99, 102, 241, 0.08)' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                <ShieldCheck className="w-4 h-4 style={{ color: '#818cf8' }}" />
                <span style={{ fontSize: '0.8125rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                  Mock Repository Analysis Scan
                </span>
                <span className="badge badge-emerald" style={{ marginLeft: 'auto' }}>PASSED</span>
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '0.5rem', fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                <div>Health Score: <strong style={{ color: '#34d399' }}>98/100</strong></div>
                <div>CVE Vulns: <strong style={{ color: '#38bdf8' }}>0 Found</strong></div>
                <div>Coverage: <strong style={{ color: '#818cf8' }}>94.2%</strong></div>
              </div>
            </div>
          </div>
        )}

        {step === 3 && (
          <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div className="input-group">
              <label className="input-label">Demo Video URL (YouTube, Vimeo, Loom) *</label>
              <input
                type="url"
                placeholder="https://youtu.be/demo-video-link"
                value={demoUrl}
                onChange={(e) => setDemoUrl(e.target.value)}
                className="input-field"
              />
            </div>

            <div className="glass-panel" style={{ padding: '1.25rem', textAlign: 'center', borderStyle: 'dashed' }}>
              <Video className="w-8 h-8 text-indigo-400" style={{ margin: '0 auto 0.5rem auto', color: '#818cf8' }} />
              <p style={{ fontSize: '0.875rem', fontWeight: 600, color: 'var(--text-primary)' }}>Video Preview Stream</p>
              <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{demoUrl || 'No video URL provided yet'}</p>
            </div>
          </div>
        )}

        {step === 4 && (
          <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div className="glass-panel" style={{ padding: '1.25rem', borderLeft: '4px solid var(--accent-emerald)' }}>
              <h3 style={{ fontSize: '1.125rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '0.5rem' }}>
                Review & Pre-Flight Finalization
              </h3>
              <p style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)', marginBottom: '1rem' }}>
                Please review your project details before locking your submission for judge assignments.
              </p>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', fontSize: '0.8125rem' }}>
                <div><strong>Title:</strong> {title}</div>
                <div><strong>Track:</strong> {trackId}</div>
                <div><strong>Repository:</strong> {repoUrl}</div>
                <div><strong>Demo Link:</strong> {demoUrl}</div>
              </div>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', background: 'rgba(245, 158, 11, 0.1)', padding: '0.75rem', borderRadius: '8px', color: '#fbbf24', fontSize: '0.75rem' }}>
              <AlertTriangle className="w-4 h-4" />
              <span>Once submitted, project details are locked for blind review processing.</span>
            </div>
          </div>
        )}

        {/* Action Controls */}
        <div style={{ marginTop: '2rem', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <button
            onClick={handleBack}
            disabled={step === 1}
            className="btn btn-secondary btn-sm"
            style={{ opacity: step === 1 ? 0.4 : 1 }}
          >
            <ChevronLeft className="w-4 h-4" />
            <span>Back</span>
          </button>

          {step < 4 ? (
            <button onClick={handleNext} className="btn btn-primary btn-sm">
              <span>Continue</span>
              <ChevronRight className="w-4 h-4" />
            </button>
          ) : (
            <button onClick={handleSubmit} className="btn btn-primary btn-sm" style={{ background: 'var(--gradient-emerald)' }}>
              <CheckCircle2 className="w-4 h-4" />
              <span>Finalize & Lock Submission</span>
            </button>
          )}
        </div>
      </div>
    </div>
  );
};
