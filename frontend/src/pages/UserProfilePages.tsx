import React from 'react';
import { User } from '../mock/types';
import { User as UserIcon, Mail, Shield, Award, Code2, Gavel, CheckCircle2 } from 'lucide-react';

export const ParticipantProfilePage: React.FC<{ user: User }> = ({ user }) => {
  const [isEditing, setIsEditing] = React.useState(false);
  const [profile, setProfile] = React.useState({
    name: user.name || 'Jane Cooper',
    email: user.email || 'participant@nova.dev',
    university: 'Stanford University (Computer Science)',
    phone: '+1 (555) 234-5678',
    avatarUrl: user.avatarUrl || 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150&auto=format&fit=crop&q=80',
    skills: 'React, TypeScript, Python, FastAPI, PostgreSQL, Docker, Tailwind',
    bio: 'Full-stack AI developer focused on agentic tool calling and real-time browser automation systems.'
  });

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    setIsEditing(false);
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* Header Profile Card */}
      <div className="glass-panel" style={{ padding: '2rem', borderRadius: '16px', background: 'var(--bg-card)' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1.25rem' }}>
            <img src={profile.avatarUrl} alt={profile.name} style={{ width: '80px', height: '80px', borderRadius: '50%', objectFit: 'cover', border: '3px solid var(--google-blue)' }} />
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
                <h1 style={{ fontSize: '1.75rem', fontWeight: 700, color: 'var(--text-primary)' }}>{profile.name}</h1>
                <span className="badge badge-cyan">PARTICIPANT</span>
              </div>
              <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>{profile.email}</p>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.25rem' }}>
                {profile.university} • {profile.phone}
              </div>
            </div>
          </div>

          <button onClick={() => setIsEditing(!isEditing)} className="btn btn-secondary">
            {isEditing ? 'Cancel Edit' : 'Edit Profile'}
          </button>
        </div>
      </div>

      {/* Edit Form OR Profile Details */}
      {isEditing ? (
        <form onSubmit={handleSave} className="glass-panel" style={{ padding: '2rem', borderRadius: '16px', display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          <h3 style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--text-primary)' }}>Edit Developer Profile</h3>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem' }}>
            <div className="input-group">
              <label className="input-label">Full Name</label>
              <input
                type="text"
                value={profile.name}
                onChange={(e) => setProfile({ ...profile, name: e.target.value })}
                className="input-field"
                required
              />
            </div>

            <div className="input-group">
              <label className="input-label">Email Address</label>
              <input
                type="email"
                value={profile.email}
                onChange={(e) => setProfile({ ...profile, email: e.target.value })}
                className="input-field"
                required
              />
            </div>

            <div className="input-group">
              <label className="input-label">University / Organization</label>
              <input
                type="text"
                value={profile.university}
                onChange={(e) => setProfile({ ...profile, university: e.target.value })}
                className="input-field"
              />
            </div>

            <div className="input-group">
              <label className="input-label">Phone Number</label>
              <input
                type="text"
                value={profile.phone}
                onChange={(e) => setProfile({ ...profile, phone: e.target.value })}
                className="input-field"
              />
            </div>
          </div>

          <div className="input-group">
            <label className="input-label">Avatar Image URL</label>
            <input
              type="url"
              value={profile.avatarUrl}
              onChange={(e) => setProfile({ ...profile, avatarUrl: e.target.value })}
              className="input-field"
            />
          </div>

          <div className="input-group">
            <label className="input-label">Skills (Comma-Separated)</label>
            <input
              type="text"
              value={profile.skills}
              onChange={(e) => setProfile({ ...profile, skills: e.target.value })}
              className="input-field"
            />
          </div>

          <div className="input-group">
            <label className="input-label">Bio & Summary</label>
            <textarea
              rows={3}
              value={profile.bio}
              onChange={(e) => setProfile({ ...profile, bio: e.target.value })}
              className="input-field"
              style={{ resize: 'vertical' }}
            />
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem', marginTop: '0.5rem' }}>
            <button type="button" onClick={() => setIsEditing(false)} className="btn btn-secondary btn-sm">
              Cancel
            </button>
            <button type="submit" className="btn btn-primary btn-sm">
              <CheckCircle2 className="w-4 h-4" />
              <span>Save Changes</span>
            </button>
          </div>
        </form>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1.5rem' }}>
          {/* Bio & Details */}
          <div className="glass-panel" style={{ padding: '1.75rem', borderRadius: '16px' }}>
            <h3 style={{ fontSize: '1.125rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '0.75rem' }}>Bio & About</h3>
            <p style={{ fontSize: '0.9375rem', color: 'var(--text-secondary)', lineHeight: 1.6, marginBottom: '1.5rem' }}>
              {profile.bio}
            </p>

            <h3 style={{ fontSize: '1.125rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '0.75rem' }}>Developer Skills</h3>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
              {profile.skills.split(',').map((skill, i) => (
                <span key={i} className="badge badge-indigo" style={{ padding: '0.375rem 0.75rem' }}>
                  {skill.trim()}
                </span>
              ))}
            </div>
          </div>

          {/* Active Event Status */}
          <div className="glass-panel" style={{ padding: '1.75rem', borderRadius: '16px' }}>
            <h3 style={{ fontSize: '1.125rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '0.75rem' }}>Registered Hackathon Status</h3>
            <div style={{ padding: '1rem', background: 'rgba(255,255,255,0.03)', borderRadius: '12px', border: '1px solid var(--border-subtle)', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
              <div style={{ fontWeight: 700, color: 'var(--text-primary)' }}>NOVA AI Innovation Challenge 2026</div>
              <div style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)' }}>Team: Quantum Crafters (Captain)</div>
              <span className="badge badge-emerald" style={{ alignSelf: 'flex-start', marginTop: '0.25rem' }}>Active Participant</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export const JudgeProfilePage: React.FC<{ user: User }> = ({ user }) => (
  <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
    <div className="glass-panel" style={{ padding: '2rem', borderRadius: '16px', background: '#292a2d' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '1.25rem' }}>
        <img src={user.avatarUrl} alt={user.name} style={{ width: '72px', height: '72px', borderRadius: '50%', objectFit: 'cover', border: '2px solid var(--google-yellow)' }} />
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
            <h1 style={{ fontSize: '1.75rem', fontWeight: 700, color: 'var(--text-primary)' }}>{user.name}</h1>
            <span className="badge badge-amber">RUBRIC JUDGE</span>
          </div>
          <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>{user.email}</p>
        </div>
      </div>
    </div>

    <div className="glass-panel" style={{ padding: '1.5rem', borderRadius: '12px', background: '#292a2d' }}>
      <h3 style={{ fontSize: '1.125rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '1rem' }}>Evaluation Credentials & Assignment Queue</h3>
      <div style={{ display: 'flex', gap: '1rem', marginBottom: '1.5rem' }}>
        <span className="badge badge-emerald"><CheckCircle2 className="w-4 h-4" /> Blind Review Certified</span>
        <span className="badge badge-indigo">Track: Developer Tools & Automation</span>
      </div>
      <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
        Assigned Hackathon: <strong>NOVA AI Innovation Challenge 2026</strong>
      </p>
    </div>
  </div>
);
