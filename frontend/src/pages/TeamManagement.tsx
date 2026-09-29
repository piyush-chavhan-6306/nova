import React, { useState } from 'react';
import { Team } from '../mock/types';
import { Users, UserPlus, Copy, Check, Shield, Mail } from 'lucide-react';

interface TeamManagementProps {
  team?: Team | null;
  hackathonName?: string;
  onAddMember: (email: string, name: string) => void;
  onCreateTeam?: (teamName: string) => void;
  onJoinTeam?: (inviteCode: string) => void;
  onOpenSubmitWizard?: () => void;
}

export const TeamManagement: React.FC<TeamManagementProps> = ({
  team,
  hackathonName,
  onAddMember,
  onCreateTeam,
  onJoinTeam,
  onOpenSubmitWizard
}) => {
  const [isInviteOpen, setIsInviteOpen] = useState(false);
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [copied, setCopied] = useState(false);

  // Form states for creating / joining team when no team exists
  const [newTeamName, setNewTeamName] = useState('');
  const [joinCode, setJoinCode] = useState('');

  const handleCopyCode = () => {
    if (team?.inviteCode) {
      navigator.clipboard.writeText(team.inviteCode);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const handleInviteSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (email && name) {
      onAddMember(email, name);
      setEmail('');
      setName('');
      setIsInviteOpen(false);
    }
  };

  const handleCreateSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (newTeamName.trim() && onCreateTeam) {
      onCreateTeam(newTeamName.trim());
      setNewTeamName('');
    }
  };

  const handleJoinSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (joinCode.trim() && onJoinTeam) {
      onJoinTeam(joinCode.trim());
      setJoinCode('');
    }
  };

  // State 1: No Team Exists
  if (!team) {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
        <div className="glass-panel" style={{ padding: '1.75rem', borderRadius: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
            <Users className="w-5 h-5 text-indigo-400" style={{ color: '#818cf8' }} />
            <h1 style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--text-primary)' }}>
              Team Formation Studio — {hackathonName || 'Hackathon'}
            </h1>
          </div>
          
          <div style={{ padding: '1rem', background: 'rgba(239, 68, 68, 0.08)', border: '1px solid rgba(239, 68, 68, 0.2)', borderRadius: '12px' }}>
            <h2 style={{ fontSize: '1.125rem', fontWeight: 700, color: '#f87171', marginBottom: '0.25rem' }}>
              You're not part of a team yet.
            </h2>
            <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
              Team membership is specific to each hackathon. To participate and submit a project for {hackathonName || 'this hackathon'}, create a new team or join an existing team using an invite code.
            </p>
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))', gap: '1.5rem' }}>
          {/* Create Team Card */}
          <div className="glass-panel" style={{ padding: '1.75rem', borderRadius: '16px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
              <UserPlus className="w-5 h-5 text-indigo-400" />
              <h2 style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                Create a New Team
              </h2>
            </div>
            <form onSubmit={handleCreateSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <div className="input-group">
                <label className="input-label">Team Name</label>
                <input
                  type="text"
                  placeholder="e.g. CyberCrafters"
                  value={newTeamName}
                  onChange={(e) => setNewTeamName(e.target.value)}
                  className="input-field"
                  required
                />
              </div>
              <button type="submit" className="btn btn-primary" style={{ padding: '0.75rem' }}>
                <Users className="w-4 h-4" />
                <span>Create Team & Generate Invite Code</span>
              </button>
            </form>
          </div>

          {/* Join Team Card */}
          <div className="glass-panel" style={{ padding: '1.75rem', borderRadius: '16px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
              <Shield className="w-5 h-5 text-emerald-400" />
              <h2 style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                Join an Existing Team
              </h2>
            </div>
            <form onSubmit={handleJoinSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <div className="input-group">
                <label className="input-label">Invite Code</label>
                <input
                  type="text"
                  placeholder="e.g. QC-2026-X9"
                  value={joinCode}
                  onChange={(e) => setJoinCode(e.target.value)}
                  className="input-field"
                  required
                />
              </div>
              <button type="submit" className="btn btn-secondary" style={{ padding: '0.75rem' }}>
                <Check className="w-4 h-4 text-emerald-400" />
                <span>Join Team with Code</span>
              </button>
            </form>
          </div>
        </div>
      </div>
    );
  }

  // Capacity calculation (Max 4 members)
  const maxCapacity = 4;
  const currentCount = team.members.length;
  const isFull = currentCount >= maxCapacity;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* Header Banner */}
      <div className="glass-panel" style={{ padding: '1.75rem', borderRadius: '16px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.375rem' }}>
            <Users className="w-5 h-5 text-indigo-400" style={{ color: '#818cf8' }} />
            <h1 style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--text-primary)' }}>
              {team.name}
            </h1>
            <span className={`badge ${isFull ? 'badge-amber' : 'badge-emerald'}`}>
              {currentCount}/{maxCapacity} Members ({isFull ? 'Team Full' : `${maxCapacity - currentCount} Spots Available`})
            </span>
          </div>
          <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
            Manage team members, roles, and invite collaborators for NOVA 2026.
          </p>
        </div>

        <div style={{ display: 'flex', gap: '0.75rem' }}>
          {!isFull && (
            <button onClick={() => setIsInviteOpen(true)} className="btn btn-secondary btn-sm">
              <UserPlus className="w-4 h-4" />
              <span>Invite Member</span>
            </button>
          )}

          {onOpenSubmitWizard && (
            <button onClick={onOpenSubmitWizard} className="btn btn-primary btn-sm">
              <Check className="w-4 h-4" />
              <span>Proceed to Project Submission</span>
            </button>
          )}
        </div>
      </div>

      {/* Invite Code Box */}
      <div className="glass-panel" style={{ padding: '1.25rem', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', background: 'rgba(99, 102, 241, 0.06)' }}>
        <div>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', fontWeight: 600 }}>Team Invite Code</span>
          <div style={{ fontSize: '1.125rem', fontWeight: 800, color: 'var(--accent-indigo)', fontFamily: 'monospace', marginTop: '0.25rem' }}>
            {team.inviteCode || 'QC-2026-X9'}
          </div>
        </div>
        <button onClick={handleCopyCode} className="btn btn-secondary btn-sm">
          {copied ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
          <span>{copied ? 'Copied Code' : 'Copy Code'}</span>
        </button>
      </div>

      {/* Team Roster Table */}
      <div className="glass-panel" style={{ padding: '1.5rem', borderRadius: '16px' }}>
        <h3 style={{ fontSize: '1.125rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '1rem' }}>
          Team Members ({team.members.length})
        </h3>

        <div className="table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th>Member</th>
                <th>Email</th>
                <th>Role</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {team.members.map((m, idx) => (
                <tr key={idx}>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      <div style={{ width: '32px', height: '32px', borderRadius: '50%', background: 'var(--gradient-primary)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#fff', fontWeight: 700, fontSize: '0.8125rem' }}>
                        {m.name.charAt(0)}
                      </div>
                      <span style={{ fontWeight: 600 }}>{m.name}</span>
                    </div>
                  </td>
                  <td style={{ color: 'var(--text-secondary)' }}>{m.email}</td>
                  <td>
                    {m.role === 'CAPTAIN' ? (
                      <span className="badge badge-indigo">
                        <Shield className="w-3 h-3" /> Captain
                      </span>
                    ) : (
                      <span className="badge badge-cyan">Member</span>
                    )}
                  </td>
                  <td>
                    <span className="badge badge-emerald">Verified</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Member Invite Modal */}
      {isInviteOpen && (
        <div style={{ position: 'fixed', inset: 0, zIndex: 200, background: 'rgba(0,0,0,0.8)', backdropFilter: 'blur(12px)', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '1rem' }}>
          <div className="glass-panel animate-fade-in" style={{ width: '100%', maxWidth: '450px', padding: '1.5rem', borderRadius: '16px' }}>
            <h3 style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '1rem' }}>
              Invite Team Member
            </h3>
            <form onSubmit={handleInviteSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <div className="input-group">
                <label className="input-label">Member Full Name</label>
                <input
                  type="text"
                  placeholder="e.g. Alex Rivera"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="input-field"
                  required
                />
              </div>

              <div className="input-group">
                <label className="input-label">Member Email Address</label>
                <input
                  type="email"
                  placeholder="alex@dev.io"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="input-field"
                  required
                />
              </div>

              <div style={{ display: 'flex', gap: '0.5rem', marginTop: '1rem', justifyContent: 'flex-end' }}>
                <button type="button" onClick={() => setIsInviteOpen(false)} className="btn btn-secondary btn-sm">
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary btn-sm">
                  <Mail className="w-4 h-4" />
                  <span>Send Invitation</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
