import React, { useState } from 'react';
import { Hackathon } from '../mock/types';
import { Trophy, Calendar, Users, EyeOff, Layers, CheckCircle2, ArrowLeft, Send } from 'lucide-react';

interface HackathonDetailsPageProps {
  hackathon: Hackathon;
  isRegistered: boolean;
  hasTeam: boolean;
  onBack: () => void;
  onOpenSubmitWizard: () => void;
  onRegister: () => void;
  onGoToTeam: () => void;
}

export const HackathonDetailsPage: React.FC<HackathonDetailsPageProps> = ({
  hackathon,
  isRegistered,
  hasTeam,
  onBack,
  onOpenSubmitWizard,
  onRegister,
  onGoToTeam
}) => {
  const [activeDetailTab, setActiveDetailTab] = useState<'OVERVIEW' | 'TIMELINE' | 'PRIZES' | 'RULES'>('OVERVIEW');

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      <button onClick={onBack} className="btn btn-secondary btn-sm" style={{ alignSelf: 'flex-start' }}>
        <ArrowLeft className="w-4 h-4" />
        <span>Back to Hackathons</span>
      </button>

      {/* Hero Banner */}
      <div className="glass-panel" style={{ borderRadius: '20px', overflow: 'hidden' }}>
        <div style={{
          height: '220px',
          background: `linear-gradient(180deg, rgba(7, 9, 14, 0.4) 0%, rgba(7, 9, 14, 0.9) 100%), url(${hackathon.bannerUrl || 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=800&auto=format&fit=crop&q=80'}) center/cover`,
          padding: '2rem',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'flex-end'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.5rem' }}>
            <span className={`badge ${hackathon.status === 'ACTIVE' ? 'badge-emerald' : hackathon.status === 'UPCOMING' ? 'badge-indigo' : 'badge-amber'}`}>
              {hackathon.status}
            </span>
            {isRegistered && (
              <span className="badge badge-emerald">
                <CheckCircle2 className="w-3.5 h-3.5" /> Registered Participant
              </span>
            )}
          </div>
          <h1 style={{ fontSize: '2.25rem', fontWeight: 800, color: 'var(--text-primary)' }}>
            {hackathon.name}
          </h1>
          <p style={{ fontSize: '1rem', color: 'var(--text-secondary)', maxWidth: '800px' }}>
            {hackathon.tagline}
          </p>
        </div>

        {/* Action Header & Key Metrics */}
        <div style={{ padding: '1.5rem 2rem', display: 'flex', flexWrap: 'wrap', alignItems: 'center', justifyContent: 'space-between', gap: '1rem', borderTop: '1px solid var(--border-subtle)' }}>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '2rem' }}>
            <div>
              <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>PRIZE POOL</span>
              <div style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--accent-amber)' }}>{hackathon.prizePool || '$50,000 USD'}</div>
            </div>
            <div>
              <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>SUBMISSIONS CLOSE</span>
              <div style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--text-primary)' }}>October 15, 2026</div>
            </div>
            <div>
              <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>PARTICIPANTS</span>
              <div style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--text-primary)' }}>{hackathon.participantCount || 0} Registered</div>
            </div>
          </div>

          <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
            {hackathon.status === 'CLOSED' ? (
              <span className="badge badge-amber" style={{ padding: '0.625rem 1.25rem', fontSize: '0.875rem' }}>
                Event Closed — Submissions Ended
              </span>
            ) : !isRegistered ? (
              <button onClick={onRegister} className="btn btn-primary" style={{ padding: '0.625rem 1.5rem' }}>
                <CheckCircle2 className="w-4 h-4" />
                <span>Register for Hackathon</span>
              </button>
            ) : !hasTeam ? (
              <button onClick={onGoToTeam} className="btn btn-primary" style={{ padding: '0.625rem 1.5rem' }}>
                <Users className="w-4 h-4" />
                <span>Registered — Create/Join Team</span>
              </button>
            ) : (
              <div style={{ display: 'flex', gap: '0.5rem' }}>
                <button onClick={onGoToTeam} className="btn btn-secondary">
                  <Users className="w-4 h-4" />
                  <span>Team Dashboard</span>
                </button>
                <button onClick={onOpenSubmitWizard} className="btn btn-primary">
                  <Send className="w-4 h-4" />
                  <span>Create Submission</span>
                </button>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Navigation Sub-Tabs */}
      <div style={{ display: 'flex', gap: '0.5rem', borderBottom: '1px solid var(--border-subtle)', paddingBottom: '0.5rem' }}>
        {[
          { id: 'OVERVIEW', label: 'Overview & Tracks' },
          { id: 'TIMELINE', label: 'Timeline & Schedule' },
          { id: 'PRIZES', label: 'Prizes & Awards' },
          { id: 'RULES', label: 'Rules & Eligibility' }
        ].map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveDetailTab(tab.id as any)}
            className={`btn btn-sm ${activeDetailTab === tab.id ? 'btn-primary' : 'btn-secondary'}`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab 1: OVERVIEW & TRACKS */}
      {activeDetailTab === 'OVERVIEW' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          {/* About Section */}
          <div className="glass-panel" style={{ padding: '1.75rem', borderRadius: '16px' }}>
            <h2 style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '0.75rem' }}>
              About the Event
            </h2>
            <p style={{ fontSize: '0.9375rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
              {hackathon.description || 'Welcome to NOVA Hackathon 2026. Join global developers, researchers, and engineers building next-generation applications. Collaborate in teams of up to 4 members, submit your open-source projects, and get evaluated by leading industry experts.'}
            </p>
          </div>

          {/* Tracks & Rubric Grid */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: '1.5rem' }}>
            {/* Challenge Tracks */}
            <div className="glass-panel" style={{ padding: '1.5rem', borderRadius: '16px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
                <Layers className="w-5 h-5 text-indigo-400" />
                <h2 style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--text-primary)' }}>Challenge Tracks</h2>
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                {hackathon.tracks && hackathon.tracks.length > 0 ? hackathon.tracks.map((t) => (
                  <div key={t.id} style={{ background: 'rgba(255, 255, 255, 0.03)', padding: '1rem', borderRadius: '12px', border: '1px solid var(--border-subtle)' }}>
                    <span className="badge badge-indigo" style={{ marginBottom: '0.375rem' }}>{t.name}</span>
                    <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>{t.description}</p>
                  </div>
                )) : (
                  <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>No tracks configured.</div>
                )}
              </div>
            </div>

            {/* Judging Rubric */}
            <div className="glass-panel" style={{ padding: '1.5rem', borderRadius: '16px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
                <Trophy className="w-5 h-5 text-amber-400" />
                <h2 style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--text-primary)' }}>Judging Criteria</h2>
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.875rem' }}>
                {hackathon.rubric && hackathon.rubric.length > 0 ? hackathon.rubric.map((r) => (
                  <div key={r.id} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0.75rem 1rem', background: 'rgba(255, 255, 255, 0.03)', borderRadius: '10px', border: '1px solid var(--border-subtle)' }}>
                    <div>
                      <div style={{ fontSize: '0.9375rem', fontWeight: 600, color: 'var(--text-primary)' }}>{r.name}</div>
                      <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{r.description}</div>
                    </div>
                    <div style={{ textAlign: 'right' }}>
                      <span className="badge badge-amber">{(r.weight * 100).toFixed(0)}% Weight</span>
                      <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginTop: '0.25rem' }}>Max {r.maxScore} Pts</div>
                    </div>
                  </div>
                )) : (
                  <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>Judging criteria configuration is pending.</div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab 2: TIMELINE */}
      {activeDetailTab === 'TIMELINE' && (
        <div className="glass-panel" style={{ padding: '1.75rem', borderRadius: '16px' }}>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '1.25rem' }}>
            Event Lifecycle Timeline
          </h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {[
              { phase: '1. Registration Window Opens', date: 'Date pending', status: 'UPCOMING' },
              { phase: '2. Hacking & Submission Period', date: `Closes: ${hackathon.submissionsClose || 'TBD'}`, status: hackathon.status === 'ACTIVE' ? 'ACTIVE' : 'UPCOMING' },
              { phase: '3. Judging Phase', date: 'Pending schedule', status: 'UPCOMING' },
            ].map((t, idx) => (
              <div key={idx} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '1rem', background: 'rgba(255,255,255,0.02)', borderRadius: '12px', border: '1px solid var(--border-subtle)' }}>
                <div>
                  <div style={{ fontWeight: 700, color: 'var(--text-primary)' }}>{t.phase}</div>
                  <div style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)' }}>{t.date}</div>
                </div>
                <span className={`badge ${t.status === 'COMPLETED' ? 'badge-emerald' : t.status === 'ACTIVE' ? 'badge-indigo' : 'badge-amber'}`}>
                  {t.status}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 3: PRIZES */}
      {activeDetailTab === 'PRIZES' && (
        <div className="glass-panel" style={{ padding: '2rem', borderRadius: '16px', textAlign: 'center' }}>
          <Trophy className="w-12 h-12 text-slate-500 mx-auto" style={{ marginBottom: '1rem' }} />
          <h3 style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--text-primary)', marginBottom: '0.5rem' }}>Checking Prize Pool</h3>
          <p style={{ fontSize: '0.9375rem', color: 'var(--text-secondary)' }}>Prize information isn't fully available yet. Check back soon.</p>
        </div>
      )}

      {/* Tab 4: RULES */}
      {activeDetailTab === 'RULES' && (
        <div className="glass-panel" style={{ padding: '1.75rem', borderRadius: '16px' }}>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '1rem' }}>
            Hackathon Rules & Eligibility Policy
          </h2>
          <ul style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', fontSize: '0.875rem', color: 'var(--text-secondary)', paddingLeft: '1.25rem' }}>
            <li><strong>Eligibility:</strong> Open to developers globally. Review event-specific restrictions.</li>
            <li><strong>Original Work:</strong> All code submitted must be created during the official hackathon window.</li>
            {hackathon.blindReviewEnabled && (
              <li><strong>Blind Review Compliance:</strong> Team identifying information is hidden from evaluators during scoring.</li>
            )}
          </ul>
        </div>
      )}
    </div>
  );
};
