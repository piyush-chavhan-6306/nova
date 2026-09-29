export type UserRole = 'PARTICIPANT' | 'JUDGE' | 'ORGANIZER' | 'ADMIN';

export interface User {
  id: string;
  name: string;
  email: string;
  role: UserRole;
  avatarUrl?: string;
  bio?: string;
}

export interface Track {
  id: string;
  name: string;
  description: string;
}

export interface RubricCriterion {
  id: string;
  name: string;
  maxScore: number;
  weight: number;
  description: string;
}

export interface Hackathon {
  id: string;
  name: string;
  tagline: string;
  status: 'DRAFT' | 'UPCOMING' | 'ACTIVE' | 'SUBMISSIONS_CLOSED' | 'CLOSED' | 'ARCHIVED';
  submissionsClose: string;
  blindReviewEnabled: boolean;
  resultsStatus: 'DRAFT' | 'CALCULATED' | 'UNDER_REVIEW' | 'APPROVED' | 'PUBLISHED' | 'LOCKED';
  tracks: Track[];
  prizes?: any[];
  rubric: RubricCriterion[];
  organizerId?: string;
  organizerName?: string;
  description?: string;
  bannerUrl?: string;
  prizePool?: string;
  participantCount?: number;
  teamCount?: number;
  submissionCount?: number;
}

export interface TeamMember {
  userId: string;
  name: string;
  email: string;
  role: 'CAPTAIN' | 'MEMBER';
}

export interface Team {
  id: string;
  name: string;
  hackathonId: string;
  inviteCode: string;
  members: TeamMember[];
}

export interface Submission {
  id: string;
  hackathonId: string;
  teamId: string;
  teamName: string;
  trackId: string;
  trackName: string;
  title: string;
  summary: string;
  description: string;
  repoUrl: string;
  demoUrl: string;
  techStack: string[];
  status: 'DRAFT' | 'SUBMITTED' | 'LOCKED';
  submittedAt: string;
  // Mock unsupported frontend features
  healthScore?: number;
  cveScanStatus?: 'PASSED' | 'WARNING' | 'FAILED';
  coveragePercent?: number;
}

export interface JudgeAssignment {
  id: string;
  judgeId: string;
  judgeName: string;
  submissionId: string;
  submissionTitle: string;
  trackName: string;
  status: 'PENDING' | 'COMPLETED';
}

export interface ScoreItem {
  criterionId: string;
  criterionName: string;
  score: number;
}

export interface Review {
  id: string;
  submissionId: string;
  judgeId: string;
  judgeName: string;
  status: 'DRAFT' | 'SUBMITTED';
  scores: ScoreItem[];
  comment: string;
  updatedAt: string;
}

export interface PairwiseEvaluation {
  id: string;
  judgeId: string;
  submissionAId: string;
  submissionATitle: string;
  submissionBId: string;
  submissionBTitle: string;
  winnerSubmissionId?: string;
  reason?: string;
  status: 'PENDING' | 'SUBMITTED';
}

export interface LeaderboardResult {
  rank: number;
  submissionId: string;
  projectTitle: string;
  teamName: string;
  trackName: string;
  rawScore: number;
  calibratedScore: number;
  pairwiseWinRate: number;
  finalRank: number;
}

export interface AuditLogItem {
  id: string;
  timestamp: string;
  actorName: string;
  actorRole: string;
  action: string;
  targetType: string;
  targetId: string;
  details: string;
}

export interface IntegrityAlert {
  id: string;
  severity: 'HIGH' | 'MEDIUM' | 'LOW';
  type: string;
  message: string;
  detectedAt: string;
}
