import React, { useState } from 'react';
import { Hackathon, User } from '../mock/types';
import { Compass, Plus, Trophy, Users, EyeOff, CheckCircle2, ArrowRight, Edit3, Lock, AlertCircle } from 'lucide-react';

interface OrganizerHackathonsPageProps {
  hackathons: Hackathon[];
  currentUser?: User | null;
  onCreateHackathon: (data: Partial<Hackathon>) => void;
  onUpdateHackathon?: (id: string, data: Partial<Hackathon>) => void;
  onSelectHackathon: (hackathon: Hackathon) => void;
}

export const OrganizerHackathonsPage: React.FC<OrganizerHackathonsPageProps> = ({
  hackathons,
  currentUser,
  onCreateHackathon,
  onUpdateHackathon,
  onSelectHackathon
}) => {
  const [isOpenModal, setIsOpenModal] = useState<boolean>(false);
  
  // Create Form State
  const [name, setName] = useState<string>('');
  const [tagline, setTagline] = useState<string>('');
  const [prizePool, setPrizePool] = useState<string>('$25,000 USD');

  // Edit State
  const [editingHackathon, setEditingHackathon] = useState<Hackathon | null>(null);
  const [activeEditTab, setActiveEditTab] = useState<'OVERVIEW' | 'TIMELINE' | 'TRACKS' | 'PRIZES' | 'RULES' | 'JUDGING'>('OVERVIEW');
  
  const [editName, setEditName] = useState<string>('');
  const [editTagline, setEditTagline] = useState<string>('');
  const [editDescription, setEditDescription] = useState<string>('');
  const [editStatus, setEditStatus] = useState<string>('ACTIVE');
  const [editSubClose, setEditSubClose] = useState<string>('');

  const handleCreateSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (name) {
      onCreateHackathon({ name, tagline, prizePool, status: 'ACTIVE' as any });
      setIsOpenModal(false);
      setName('');
      setTagline('');
    }
  };

  const handleOpenEdit = (h: Hackathon) => {
    setEditingHackathon(h);
    setActiveEditTab('OVERVIEW');
    setEditName(h.name);
    setEditTagline(h.tagline || '');
    setEditDescription(h.description || '');
    setEditStatus(h.status);
    setEditSubClose(h.submissionsClose || '');
  };

  const handleEditSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (editingHackathon && onUpdateHackathon) {
      onUpdateHackathon(editingHackathon.id, {
        name: editName,
        tagline: editTagline, // Note: not persisted by real backend yet
        description: editDescription,
        status: editStatus as any,
        submissionsClose: editSubClose
      });
      setEditingHackathon(null);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      <div className="glass-panel glass-panel-glow" style={{ padding: '2rem', borderRadius: '20px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
              <Compass className="w-5 h-5 text-emerald-400" />
              <span style={{ fontSize: '0.8125rem', fontWeight: 700, color: '#34d399', textTransform: 'uppercase' }}>
                ORGANIZER EVENTS MANAGEMENT
              </span>
            </div>
            <h1 style={{ fontSize: '2rem', fontWeight: 800, color: 'var(--text-primary)' }}>
              My Managed Hackathons ({hackathons.length})
            </h1>
            <p style={{ fontSize: '0.9375rem', color: 'var(--text-secondary)' }}>
              Organize, configure, and operate hackathon events under your organizer ownership scope.
            </p>
          </div>

          <button onClick={() => setIsOpenModal(true)} className="btn btn-primary">
            <Plus className="w-4 h-4" />
            <span>Create New Hackathon</span>
          </button>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(360px, 1fr))', gap: '1.5rem' }}>
        {hackathons.map((h) => {
          const isOwner = currentUser?.role === 'ADMIN' || !h.organizerId || h.organizerId === currentUser?.id || currentUser?.role === 'ORGANIZER';

          return (
            <div key={h.id} className="glass-panel" style={{ borderRadius: '18px', overflow: 'hidden', padding: '1.5rem', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
              <div>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
                  <span className="badge badge-emerald">{h.status}</span>
                  {isOwner ? (
                    <span className="badge badge-indigo">
                      Owner: {h.organizerName || 'Alex Organizer'}
                    </span>
                  ) : (
                    <span className="badge badge-amber">
                      <Lock className="w-3 h-3" /> View Only
                    </span>
                  )}
                </div>

                <h3 style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '0.375rem' }}>
                  {h.name}
                </h3>
                <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', marginBottom: '1.25rem' }}>
                  {h.tagline}
                </p>

                <div style={{ display: 'flex', gap: '1rem', fontSize: '0.8125rem', color: 'var(--text-muted)', marginBottom: '1.25rem' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.375rem' }}>
                    <Trophy className="w-4 h-4 text-amber-400" />
                    <span>{h.prizePool || '$50,000'}</span>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.375rem' }}>
                    <Users className="w-4 h-4 text-indigo-400" />
                    <span>{h.participantCount || 0} Participants</span>
                  </div>
                </div>
              </div>

              <div style={{ display: 'flex', gap: '0.5rem', marginTop: '1rem' }}>
                <button onClick={() => onSelectHackathon(h)} className="btn btn-secondary btn-sm" style={{ flex: 1 }}>
                  <span>Command Center</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>

                {isOwner && onUpdateHackathon && (
                  <button onClick={() => handleOpenEdit(h)} className="btn btn-primary btn-sm">
                    <Edit3 className="w-3.5 h-3.5" />
                    <span>Edit Event</span>
                  </button>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {isOpenModal && (
        <div style={{ position: 'fixed', inset: 0, zIndex: 200, background: 'rgba(0,0,0,0.8)', backdropFilter: 'blur(12px)', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '1rem' }}>
          <div className="glass-panel" style={{ width: '100%', maxWidth: '540px', padding: '2rem', borderRadius: '20px' }}>
            <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--text-primary)', marginBottom: '1rem' }}>
              Create New Hackathon Event
            </h2>
            <form onSubmit={handleCreateSubmit}>
              <div className="input-group">
                <label className="input-label">Hackathon Name</label>
                <input type="text" value={name} onChange={(e) => setName(e.target.value)} className="input-field" required />
              </div>
              <div className="input-group">
                <label className="input-label">Tagline & Summary</label>
                <input type="text" value={tagline} onChange={(e) => setTagline(e.target.value)} className="input-field" required />
              </div>
              <div style={{ display: 'flex', gap: '1rem', justifyContent: 'flex-end', marginTop: '1.5rem' }}>
                <button type="button" onClick={() => setIsOpenModal(false)} className="btn btn-secondary btn-sm">Cancel</button>
                <button type="submit" className="btn btn-primary btn-sm">Create Event</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {editingHackathon && (
        <div style={{ position: 'fixed', inset: 0, zIndex: 200, background: 'rgba(0,0,0,0.8)', backdropFilter: 'blur(12px)', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '1rem' }}>
          <div className="glass-panel animate-fade-in" style={{ width: '100%', maxWidth: '800px', maxHeight: '90vh', overflowY: 'auto', padding: '2rem', borderRadius: '20px' }}>
            
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.5rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                <Edit3 className="w-6 h-6 text-indigo-400" />
                <div>
                  <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--text-primary)' }}>
                    Manage Hackathon Details
                  </h2>
                  <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                    Editing {editingHackathon.name}
                  </p>
                </div>
              </div>
              <button onClick={() => setEditingHackathon(null)} className="btn btn-secondary btn-sm">Close</button>
            </div>

            <div style={{ display: 'flex', gap: '0.5rem', borderBottom: '1px solid var(--border-subtle)', paddingBottom: '0.75rem', marginBottom: '1.5rem', overflowX: 'auto' }}>
              {[
                { id: 'OVERVIEW', label: 'Overview' },
                { id: 'TRACKS', label: 'Tracks' },
                { id: 'TIMELINE', label: 'Timeline' },
                { id: 'PRIZES', label: 'Prizes' },
                { id: 'RULES', label: 'Rules' },
                { id: 'JUDGING', label: 'Judging' }
              ].map(tab => (
                <button 
                  key={tab.id}
                  onClick={() => setActiveEditTab(tab.id as any)}
                  className={`btn btn-sm ${activeEditTab === tab.id ? 'btn-primary' : 'btn-secondary'}`}
                  style={{ whiteSpace: 'nowrap' }}
                >
                  {tab.label}
                </button>
              ))}
            </div>

            <form onSubmit={handleEditSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', minHeight: '300px' }}>
              
              {activeEditTab === 'OVERVIEW' && (
                <>
                  <div className="input-group">
                    <label className="input-label">Hackathon Name</label>
                    <input type="text" value={editName} onChange={(e) => setEditName(e.target.value)} className="input-field" required />
                  </div>
                  <div className="input-group" style={{ opacity: 0.7 }}>
                    <label className="input-label">Tagline</label>
                    <input type="text" value={editTagline} onChange={(e) => setEditTagline(e.target.value)} className="input-field" placeholder="Tagline support is pending" disabled />
                  </div>
                  <div className="input-group">
                    <label className="input-label">About & Description</label>
                    <textarea rows={4} value={editDescription} onChange={(e) => setEditDescription(e.target.value)} className="input-field" style={{ resize: 'vertical' }} />
                  </div>
                  <div className="input-group">
                    <label className="input-label">Status</label>
                    <select value={editStatus} onChange={(e) => setEditStatus(e.target.value)} className="input-field">
                      <option value="DRAFT">DRAFT</option>
                      <option value="UPCOMING">UPCOMING</option>
                      <option value="ACTIVE">ACTIVE</option>
                      <option value="SUBMISSIONS_CLOSED">SUBMISSIONS_CLOSED</option>
                      <option value="CLOSED">CLOSED</option>
                    </select>
                  </div>
                </>
              )}

              {activeEditTab === 'TRACKS' && (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                  <div style={{ padding: '1rem', background: 'rgba(255, 255, 255, 0.03)', border: '1px solid var(--border-subtle)', borderRadius: '12px', display: 'flex', gap: '0.75rem' }}>
                    <AlertCircle className="w-5 h-5 text-indigo-400 flex-shrink-0" />
                    <div>
                      <p style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)', margin: 0 }}>
                        Existing tracks are currently view-only. You can create new tracks through the platform API.
                      </p>
                    </div>
                  </div>
                  
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                    <h3 style={{ fontSize: '1rem', fontWeight: 600, color: 'var(--text-primary)' }}>Current Tracks (Read Only)</h3>
                    {editingHackathon.tracks.map(t => (
                      <div key={t.id} style={{ padding: '0.75rem 1rem', background: 'rgba(255,255,255,0.03)', borderRadius: '8px', border: '1px solid var(--border-subtle)' }}>
                        <div style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{t.name}</div>
                        <div style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)' }}>{t.description}</div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {activeEditTab === 'TIMELINE' && (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                  <div className="input-group">
                    <label className="input-label">Submissions Close Date (ISO String)</label>
                    <input type="text" value={editSubClose} onChange={(e) => setEditSubClose(e.target.value)} className="input-field" placeholder="e.g. 2026-10-15T23:59:59Z" />
                  </div>
                  <div style={{ padding: '1rem', background: 'rgba(255, 255, 255, 0.02)', borderRadius: '8px', border: '1px solid var(--border-subtle)' }}>
                    <p style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)', margin: 0 }}>
                      Only basic registration and submission close dates are supported for this event type.
                    </p>
                  </div>
                </div>
              )}

              {activeEditTab === 'PRIZES' && (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                  <div style={{ padding: '1rem', background: 'rgba(255, 255, 255, 0.03)', border: '1px solid var(--border-subtle)', borderRadius: '12px', display: 'flex', gap: '0.75rem' }}>
                    <AlertCircle className="w-5 h-5 text-indigo-400 flex-shrink-0" />
                    <div>
                      <p style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)', margin: 0 }}>
                        Existing prizes are currently view-only. You can create or manage prizes through the platform API.
                      </p>
                    </div>
                  </div>
                  
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                    <h3 style={{ fontSize: '1rem', fontWeight: 600, color: 'var(--text-primary)' }}>Current Prizes (Read Only)</h3>
                    {(editingHackathon.prizes || []).length > 0 ? (
                      editingHackathon.prizes!.map((p: any) => (
                        <div key={p.id} style={{ padding: '0.75rem 1rem', background: 'rgba(255,255,255,0.03)', borderRadius: '8px', border: '1px solid var(--border-subtle)' }}>
                          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                            <div style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{p.name}</div>
                            <div style={{ fontSize: '0.8125rem', color: 'var(--text-emerald)', fontWeight: 'bold' }}>{p.value}</div>
                          </div>
                          <div style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)' }}>{p.description}</div>
                        </div>
                      ))
                    ) : (
                      <div style={{ padding: '2rem', textAlign: 'center', background: 'rgba(255, 255, 255, 0.02)', borderRadius: '12px', border: '1px dashed var(--border-subtle)' }}>
                        <Trophy className="w-8 h-8 text-slate-400 mx-auto" style={{ marginBottom: '1rem' }} />
                        <p style={{ fontSize: '0.9375rem', color: 'var(--text-secondary)' }}>No prizes configured for this event yet.</p>
                      </div>
                    )}
                  </div>
                </div>
              )}
              {activeEditTab === 'RULES' && (
                <div style={{ padding: '2rem', textAlign: 'center', background: 'rgba(255, 255, 255, 0.02)', borderRadius: '12px', border: '1px dashed var(--border-subtle)' }}>
                  <EyeOff className="w-8 h-8 text-slate-400 mx-auto" style={{ marginBottom: '1rem' }} />
                  <p style={{ fontSize: '0.9375rem', color: 'var(--text-secondary)' }}>Rules haven't been configured for this event yet.</p>
                </div>
              )}
              {activeEditTab === 'JUDGING' && (
                <div style={{ padding: '2rem', textAlign: 'center', background: 'rgba(255, 255, 255, 0.02)', borderRadius: '12px', border: '1px dashed var(--border-subtle)' }}>
                  <AlertCircle className="w-8 h-8 text-slate-400 mx-auto" style={{ marginBottom: '1rem' }} />
                  <p style={{ fontSize: '0.9375rem', color: 'var(--text-secondary)' }}>Judging configuration is currently locked.</p>
                </div>
              )}

              <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: 'auto', paddingTop: '1rem', borderTop: '1px solid var(--border-subtle)' }}>
                <button type="submit" className="btn btn-primary">
                  <CheckCircle2 className="w-4 h-4" />
                  <span>Save Hackathon Changes</span>
                </button>
              </div>
            </form>
            
          </div>
        </div>
      )}
    </div>
  );
};
