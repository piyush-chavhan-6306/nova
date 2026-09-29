import React, { useState } from 'react';
import { JudgeAssignment, Submission, Hackathon } from '../mock/types';
import { Gavel, CheckCircle2, Clock, EyeOff, Search } from 'lucide-react';

interface JudgeAssignmentsPageProps {
  assignments: JudgeAssignment[];
  submissions: Submission[];
  hackathon: Hackathon;
  onOpenEvaluation: (submissionId: string) => void;
}

export const JudgeAssignmentsPage: React.FC<JudgeAssignmentsPageProps> = ({
  assignments,
  submissions,
  hackathon,
  onOpenEvaluation
}) => {
  const [filter, setFilter] = useState<'ALL' | 'PENDING' | 'COMPLETED'>('ALL');

  const filteredAssignments = assignments.filter(a => {
    if (filter === 'PENDING') return a.status === 'PENDING';
    if (filter === 'COMPLETED') return a.status === 'COMPLETED';
    return true;
  });

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      <div className="glass-panel glass-panel-glow" style={{ padding: '2rem', borderRadius: '20px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
          <Gavel className="w-5 h-5 text-amber-400" />
          <span style={{ fontSize: '0.8125rem', fontWeight: 700, color: '#fbbf24', textTransform: 'uppercase' }}>
            JUDGE ASSIGNMENTS QUEUE
          </span>
        </div>
        <h1 style={{ fontSize: '2rem', fontWeight: 800, color: 'var(--text-primary)' }}>
          My Assigned Projects ({assignments.length})
        </h1>
        <p style={{ fontSize: '0.9375rem', color: 'var(--text-secondary)' }}>
          Evaluate assigned hackathon submissions. Blind review is enforced to anonymize team identities.
        </p>
      </div>

      <div style={{ display: 'flex', gap: '0.5rem' }}>
        {(['ALL', 'PENDING', 'COMPLETED'] as const).map(st => (
          <button
            key={st}
            onClick={() => setFilter(st)}
            className={`btn btn-sm ${filter === st ? 'btn-primary' : 'btn-secondary'}`}
          >
            {st}
          </button>
        ))}
      </div>

      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>Project Title</th>
              <th>Track</th>
              <th>Team (Blind Mode)</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {filteredAssignments.map(asg => {
              const sub = submissions.find(s => s.id === asg.submissionId);
              const isDone = asg.status === 'COMPLETED';
              return (
                <tr key={asg.id}>
                  <td style={{ fontWeight: 700, color: 'var(--text-primary)' }}>{asg.submissionTitle}</td>
                  <td><span className="badge badge-indigo">{asg.trackName}</span></td>
                  <td style={{ color: 'var(--text-muted)' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.375rem' }}>
                      <EyeOff className="w-3.5 h-3.5 text-amber-400" />
                      <span>{hackathon.blindReviewEnabled ? 'Anonymous Team' : sub?.teamName}</span>
                    </div>
                  </td>
                  <td>
                    {isDone ? (
                      <span className="badge badge-emerald"><CheckCircle2 className="w-3.5 h-3.5" /> Completed</span>
                    ) : (
                      <span className="badge badge-amber"><Clock className="w-3.5 h-3.5" /> Pending</span>
                    )}
                  </td>
                  <td>
                    <button onClick={() => onOpenEvaluation(asg.submissionId)} className="btn btn-secondary btn-sm">
                      {isDone ? 'Edit Review' : 'Evaluate'}
                    </button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};
