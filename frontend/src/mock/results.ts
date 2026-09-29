import type { LeaderboardResult, PairwiseEvaluation, AuditLogItem, IntegrityAlert } from './types';

export const MOCK_LEADERBOARD: LeaderboardResult[] = [
  {
    rank: 1,
    submissionId: 'prj_01',
    projectTitle: 'Quiet Hours',
    teamName: 'Quantum Crafters',
    trackName: 'Developer Tools & Automation',
    rawScore: 9.15,
    calibratedScore: 9.38,
    pairwiseWinRate: 92.5,
    finalRank: 1
  },
  {
    rank: 2,
    submissionId: 'prj_02',
    projectTitle: 'Glass Signal',
    teamName: 'CyberForge Labs',
    trackName: 'Artificial Intelligence & Agents',
    rawScore: 8.85,
    calibratedScore: 8.92,
    pairwiseWinRate: 85.0,
    finalRank: 2
  },
  {
    rank: 3,
    submissionId: 'prj_03',
    projectTitle: 'Deep Compass',
    teamName: 'Zero Knowledge Guild',
    trackName: 'Web3 & Decentralized Infrastructure',
    rawScore: 8.40,
    calibratedScore: 8.55,
    pairwiseWinRate: 78.0,
    finalRank: 3
  }
];

export const MOCK_PAIRWISE_EVALUATIONS: PairwiseEvaluation[] = [
  {
    id: 'pw_01',
    judgeId: 'jdg_01',
    submissionAId: 'prj_01',
    submissionATitle: 'Quiet Hours',
    submissionBId: 'prj_02',
    submissionBTitle: 'Glass Signal',
    winnerSubmissionId: 'prj_01',
    reason: 'Quiet Hours demonstrated higher architectural maturity and production readiness.',
    status: 'SUBMITTED'
  },
  {
    id: 'pw_02',
    judgeId: 'jdg_01',
    submissionAId: 'prj_02',
    submissionATitle: 'Glass Signal',
    submissionBId: 'prj_03',
    submissionBTitle: 'Deep Compass',
    status: 'PENDING'
  }
];

export const MOCK_AUDIT_LOGS: AuditLogItem[] = [
  {
    id: 'log_01',
    timestamp: '2026-09-28T22:10:05Z',
    actorName: 'Ada Okonkwo',
    actorRole: 'JUDGE',
    action: 'REVIEW_SUBMITTED',
    targetType: 'Submission',
    targetId: 'prj_01',
    details: 'Submitted score review (9.15/10) for Quiet Hours.'
  },
  {
    id: 'log_02',
    timestamp: '2026-09-28T21:45:00Z',
    actorName: 'Alex Organizer',
    actorRole: 'ORGANIZER',
    action: 'BLIND_REVIEW_ENABLED',
    targetType: 'Hackathon',
    targetId: 'evt_01',
    details: 'Enabled blind review anonymization mode.'
  },
  {
    id: 'log_03',
    timestamp: '2026-09-28T20:30:12Z',
    actorName: 'Priya Participant',
    actorRole: 'PARTICIPANT',
    action: 'SUBMISSION_FINALIZED',
    targetType: 'Submission',
    targetId: 'prj_01',
    details: 'Finalized and locked submission details for Quiet Hours.'
  }
];

export const MOCK_INTEGRITY_ALERTS: IntegrityAlert[] = [
  {
    id: 'alt_01',
    severity: 'LOW',
    type: 'SCORE_VARIANCE',
    message: 'Judge B standard deviation (+2.1) is higher than event mean. Automatic calibration active.',
    detectedAt: '2026-09-28T22:00:00Z'
  },
  {
    id: 'alt_02',
    severity: 'MEDIUM',
    type: 'RECUSAL_LOGGED',
    message: 'Judge Conflict declared for Project #prj_04 (Aether Systems). Judge assignment revoked.',
    detectedAt: '2026-09-28T21:15:00Z'
  }
];
