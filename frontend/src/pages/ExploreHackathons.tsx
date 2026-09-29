import React, { useState, useEffect } from 'react';
import { Hackathon } from '../mock/types';
import { mockService } from '../services/mockService';
import { Search, Compass, Calendar, Trophy, Users, EyeOff, ArrowRight } from 'lucide-react';

interface ExploreHackathonsProps {
  onSelectHackathon: (hackathon: Hackathon) => void;
}

export const ExploreHackathons: React.FC<ExploreHackathonsProps> = ({ onSelectHackathon }) => {
  const [hackathons, setHackathons] = useState<Hackathon[]>([]);
  const [search, setSearch] = useState<string>('');
  const [statusFilter, setStatusFilter] = useState<string>('ALL');

  useEffect(() => {
    loadHackathons();
  }, [search, statusFilter]);

  const loadHackathons = async () => {
    const list = await mockService.getHackathons(search, statusFilter);
    setHackathons(list);
  };

  const getStatusBadge = (status: Hackathon['status']) => {
    switch (status) {
      case 'ACTIVE': return <span className="badge badge-emerald">ACTIVE & OPEN</span>;
      case 'UPCOMING': return <span className="badge badge-cyan">UPCOMING</span>;
      case 'CLOSED': return <span className="badge badge-amber">COMPLETED</span>;
      default: return <span className="badge badge-indigo">{status}</span>;
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* Header Banner */}
      <div className="glass-panel glass-panel-glow" style={{ padding: '2rem', borderRadius: '20px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
          <Compass className="w-5 h-5 text-indigo-400" />
          <span style={{ fontSize: '0.8125rem', fontWeight: 700, color: '#818cf8', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            HACKATHON DISCOVERY
          </span>
        </div>
        <h1 style={{ fontSize: '2rem', fontWeight: 800, color: 'var(--text-primary)', marginBottom: '0.5rem' }}>
          Explore Open Hackathons
        </h1>
        <p style={{ fontSize: '0.9375rem', color: 'var(--text-secondary)', maxWidth: '700px' }}>
          Browse active challenges, filter by tracks, join teams, and submit solutions to win prizes.
        </p>
      </div>

      {/* Filter & Search Bar */}
      <div style={{ display: 'flex', flexWrap: 'wrap', alignItems: 'center', justifyContent: 'space-between', gap: '1rem' }}>
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          {['ALL', 'ACTIVE', 'UPCOMING', 'CLOSED'].map((st) => (
            <button
              key={st}
              onClick={() => setStatusFilter(st)}
              className={`btn btn-sm ${statusFilter === st ? 'btn-primary' : 'btn-secondary'}`}
            >
              {st}
            </button>
          ))}
        </div>

        <div style={{ position: 'relative', minWidth: '280px' }}>
          <Search className="w-4 h-4" style={{ position: 'absolute', left: '0.75rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
          <input
            type="text"
            placeholder="Search hackathons by keyword..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="input-field"
            style={{ paddingLeft: '2.25rem', height: '38px' }}
          />
        </div>
      </div>

      {/* Hackathon Cards Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(360px, 1fr))', gap: '1.5rem' }}>
        {hackathons.map((h) => (
          <div key={h.id} className="glass-panel" style={{ borderRadius: '18px', overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
            <div style={{ height: '140px', background: `url(${h.bannerUrl || 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=800&auto=format&fit=crop&q=80'}) center/cover`, position: 'relative' }}>
              <div style={{ position: 'absolute', top: '1rem', right: '1rem' }}>
                {getStatusBadge(h.status)}
              </div>
            </div>

            <div style={{ padding: '1.5rem', flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
              <div>
                <h3 style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '0.375rem' }}>
                  {h.name}
                </h3>
                <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', lineHeight: 1.4, marginBottom: '1rem' }}>
                  {h.tagline}
                </p>

                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.75rem', marginBottom: '1.25rem', fontSize: '0.8125rem', color: 'var(--text-muted)' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.375rem' }}>
                    <Trophy className="w-4 h-4 text-amber-400" />
                    <span>{h.prizePool || '$50,000 USD'}</span>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.375rem' }}>
                    <Users className="w-4 h-4 text-indigo-400" />
                    <span>{h.participantCount || 100}+ Participants</span>
                  </div>
                  {h.blindReviewEnabled && (
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.375rem' }}>
                      <EyeOff className="w-4 h-4 text-emerald-400" />
                      <span>Blind Review</span>
                    </div>
                  )}
                </div>
              </div>

              <div style={{ paddingTop: '1rem', borderTop: '1px solid var(--border-subtle)', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                  Organized by {h.organizerName || 'Alex Organizer'}
                </span>
                <button onClick={() => onSelectHackathon(h)} className="btn btn-secondary btn-sm">
                  <span>View Details</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
