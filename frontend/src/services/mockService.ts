import type { UserRole, User, Hackathon, Team, Submission, JudgeAssignment, Review, PairwiseEvaluation, LeaderboardResult, AuditLogItem, IntegrityAlert } from '../mock/types';
import { MOCK_USERS } from '../mock/users';
import { MOCK_HACKATHONS } from '../mock/hackathons';
import { MOCK_TEAMS } from '../mock/teams';
import { MOCK_SUBMISSIONS } from '../mock/submissions';
import { MOCK_JUDGE_ASSIGNMENTS, MOCK_REVIEWS } from '../mock/reviews';
import { MOCK_LEADERBOARD, MOCK_PAIRWISE_EVALUATIONS, MOCK_AUDIT_LOGS, MOCK_INTEGRITY_ALERTS } from '../mock/results';

class MockService {
  private users = { ...MOCK_USERS };
  private hackathons: Hackathon[] = [...MOCK_HACKATHONS];
  private teams: Team[] = [...MOCK_TEAMS];
  private submissions: Submission[] = [...MOCK_SUBMISSIONS];
  private judgeAssignments: JudgeAssignment[] = [...MOCK_JUDGE_ASSIGNMENTS];
  private reviews: Review[] = [...MOCK_REVIEWS];
  private pairwiseEvaluations: PairwiseEvaluation[] = [...MOCK_PAIRWISE_EVALUATIONS];
  private leaderboard: LeaderboardResult[] = [...MOCK_LEADERBOARD];
  private auditLogs: AuditLogItem[] = [...MOCK_AUDIT_LOGS];
  private alerts: IntegrityAlert[] = [...MOCK_INTEGRITY_ALERTS];

  // User & Auth Role
  async getCurrentUser(role: UserRole): Promise<User> {
    return this.users[role] || this.users.PARTICIPANT;
  }

  async getAllUsers(): Promise<User[]> {
    return Object.values(this.users);
  }

  async getUsersByRole(role: UserRole): Promise<User[]> {
    return Object.values(this.users).filter(u => u.role === role);
  }

  // Hackathon Meta & Discovery
  async getHackathon(): Promise<Hackathon> {
    return { ...this.hackathons[0] };
  }

  async getHackathons(search?: string, status?: string): Promise<Hackathon[]> {
    let list = [...this.hackathons];
    if (status && status !== 'ALL') {
      list = list.filter(h => h.status === status);
    }
    if (search) {
      const q = search.toLowerCase();
      list = list.filter(h => h.name.toLowerCase().includes(q) || h.tagline.toLowerCase().includes(q));
    }
    return list;
  }

  async getHackathonById(id: string): Promise<Hackathon | undefined> {
    return this.hackathons.find(h => h.id === id) || this.hackathons[0];
  }

  async createHackathon(data: Partial<Hackathon>, organizerId: string): Promise<Hackathon> {
    const newHack: Hackathon = {
      id: `evt_0${this.hackathons.length + 1}`,
      name: data.name || 'New Hackathon 2026',
      tagline: data.tagline || 'Building the future of technology.',
      status: data.status || 'ACTIVE',
      submissionsClose: data.submissionsClose || '2026-11-30T23:59:59Z',
      blindReviewEnabled: data.blindReviewEnabled ?? true,
      resultsStatus: 'DRAFT',
      organizerId,
      organizerName: 'Alex Organizer',
      bannerUrl: 'https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=800&auto=format&fit=crop&q=80',
      prizePool: data.prizePool || '$20,000 USD',
      participantCount: 1,
      teamCount: 1,
      submissionCount: 0,
      tracks: data.tracks || [
        { id: `trk_${Date.now()}`, name: 'General Innovation', description: 'Open track for innovative software.' }
      ],
      rubric: this.hackathons[0].rubric
    };

    this.hackathons.unshift(newHack);
    this.addAuditLog('ORGANIZER', 'Alex Organizer', 'HACKATHON_CREATED', 'Hackathon', newHack.id, `Created hackathon ${newHack.name}`);
    return newHack;
  }

  async updateHackathon(id: string, data: Partial<Hackathon>): Promise<Hackathon> {
    const idx = this.hackathons.findIndex(h => h.id === id);
    if (idx !== -1) {
      this.hackathons[idx] = { ...this.hackathons[idx], ...data };
      this.addAuditLog('ORGANIZER', 'Alex Organizer', 'HACKATHON_UPDATED', 'Hackathon', id, `Updated hackathon details for ${this.hackathons[idx].name}`);
      return this.hackathons[idx];
    }
    this.hackathons[0] = { ...this.hackathons[0], ...data };
    return this.hackathons[0];
  }

  async toggleBlindReview(hackathonId?: string): Promise<boolean> {
    const target = this.hackathons.find(h => h.id === (hackathonId || 'evt_01')) || this.hackathons[0];
    target.blindReviewEnabled = !target.blindReviewEnabled;
    this.addAuditLog('ORGANIZER', 'Alex Organizer', 'TOGGLE_BLIND_REVIEW', 'Hackathon', target.id, `Blind review set to ${target.blindReviewEnabled}`);
    return target.blindReviewEnabled;
  }

  // Submissions & Gallery
  async getSubmissions(trackId?: string, search?: string): Promise<Submission[]> {
    let list = [...this.submissions];
    if (trackId && trackId !== 'all') {
      list = list.filter(s => s.trackId === trackId);
    }
    if (search) {
      const q = search.toLowerCase();
      list = list.filter(s => s.title.toLowerCase().includes(q) || s.summary.toLowerCase().includes(q) || s.techStack.some(t => t.toLowerCase().includes(q)));
    }
    return list;
  }

  async getSubmissionById(id: string): Promise<Submission | undefined> {
    return this.submissions.find(s => s.id === id);
  }

  async createOrUpdateSubmission(sub: Partial<Submission>): Promise<Submission> {
    const existingIndex = this.submissions.findIndex(s => s.id === sub.id);
    if (existingIndex >= 0) {
      this.submissions[existingIndex] = { ...this.submissions[existingIndex], ...sub } as Submission;
      this.addAuditLog('PARTICIPANT', 'Priya Sharma', 'SUBMISSION_UPDATED', 'Submission', sub.id!, `Updated ${sub.title}`);
      return this.submissions[existingIndex];
    } else {
      const newSub: Submission = {
        id: `prj_0${this.submissions.length + 1}`,
        hackathonId: sub.hackathonId || 'evt_01',
        teamId: sub.teamId || 'team_01',
        teamName: sub.teamName || 'Quantum Crafters',
        trackId: sub.trackId || 'trk_01',
        trackName: sub.trackName || 'Developer Tools & Automation',
        title: sub.title || 'Untitled Project',
        summary: sub.summary || '',
        description: sub.description || '',
        repoUrl: sub.repoUrl || 'https://github.com/example/repo',
        demoUrl: sub.demoUrl || 'https://youtu.be/demo',
        techStack: sub.techStack || ['React', 'TypeScript', 'Python'],
        status: sub.status || 'SUBMITTED',
        submittedAt: new Date().toISOString(),
        healthScore: 95,
        cveScanStatus: 'PASSED',
        coveragePercent: 91.0
      };
      this.submissions.unshift(newSub);
      this.addAuditLog('PARTICIPANT', 'Priya Sharma', 'SUBMISSION_CREATED', 'Submission', newSub.id, `Created project ${newSub.title}`);
      return newSub;
    }
  }

  // Teams
  async getTeams(): Promise<Team[]> {
    return [...this.teams];
  }

  async addTeamMember(teamId: string, email: string, name: string): Promise<Team> {
    const team = this.teams.find(t => t.id === teamId);
    if (team) {
      team.members.push({ userId: `usr_${Date.now()}`, name, email, role: 'MEMBER' });
      this.addAuditLog('PARTICIPANT', name, 'MEMBER_INVITED', 'Team', teamId, `Invited ${email} to ${team.name}`);
    }
    return { ...team! };
  }

  // Judging
  async getJudgeAssignments(judgeId: string): Promise<JudgeAssignment[]> {
    return this.judgeAssignments.filter(a => a.judgeId === judgeId || judgeId === 'usr_judge_001');
  }

  async getReview(submissionId: string, judgeId: string): Promise<Review | undefined> {
    return this.reviews.find(r => r.submissionId === submissionId && (r.judgeId === judgeId || judgeId === 'usr_judge_001'));
  }

  async saveReview(submissionId: string, judgeId: string, scores: { criterionId: string; criterionName: string; score: number }[], comment: string, isSubmit: boolean): Promise<Review> {
    let rev = this.reviews.find(r => r.submissionId === submissionId && r.judgeId === judgeId);
    if (!rev) {
      rev = {
        id: `rev_0${this.reviews.length + 1}`,
        submissionId,
        judgeId,
        judgeName: 'Dr. Ada Okonkwo',
        status: isSubmit ? 'SUBMITTED' : 'DRAFT',
        scores,
        comment,
        updatedAt: new Date().toISOString()
      };
      this.reviews.push(rev);
    } else {
      rev.scores = scores;
      rev.comment = comment;
      rev.status = isSubmit ? 'SUBMITTED' : 'DRAFT';
      rev.updatedAt = new Date().toISOString();
    }

    if (isSubmit) {
      const asg = this.judgeAssignments.find(a => a.submissionId === submissionId);
      if (asg) asg.status = 'COMPLETED';
      this.addAuditLog('JUDGE', 'Dr. Ada Okonkwo', 'REVIEW_SUBMITTED', 'Submission', submissionId, `Submitted review score for ${submissionId}`);
    }
    return { ...rev };
  }

  // Pairwise
  async getPairwiseEvaluations(judgeId: string): Promise<PairwiseEvaluation[]> {
    return this.pairwiseEvaluations.filter(p => p.judgeId === judgeId || judgeId === 'usr_judge_001');
  }

  async submitPairwiseDecision(evalId: string, winnerId: string, reason: string): Promise<PairwiseEvaluation> {
    const item = this.pairwiseEvaluations.find(p => p.id === evalId);
    if (item) {
      item.winnerSubmissionId = winnerId;
      item.reason = reason;
      item.status = 'SUBMITTED';
      this.addAuditLog('JUDGE', 'Dr. Ada Okonkwo', 'PAIRWISE_SUBMITTED', 'Pairwise', evalId, `Selected winner ${winnerId}`);
    }
    return { ...item! };
  }

  // Results & Leaderboards
  async getLeaderboard(): Promise<LeaderboardResult[]> {
    return [...this.leaderboard];
  }

  async updateResultsStatus(status: Hackathon['resultsStatus']): Promise<Hackathon['resultsStatus']> {
    this.hackathons[0].resultsStatus = status;
    this.addAuditLog('ORGANIZER', 'Alex Organizer', 'RESULTS_STATUS_CHANGED', 'Hackathon', 'evt_01', `Status transitioned to ${status}`);
    return this.hackathons[0].resultsStatus;
  }

  // Admin Platform Stats
  async getAdminStats() {
    return {
      totalHackathons: this.hackathons.length,
      activeHackathons: this.hackathons.filter(h => h.status === 'ACTIVE').length,
      totalParticipants: 650,
      totalOrganizers: 12,
      totalJudges: 18,
      totalSubmissions: 128
    };
  }

  // Audit & Analytics
  async getAuditLogs(): Promise<AuditLogItem[]> {
    return [...this.auditLogs];
  }

  async getIntegrityAlerts(): Promise<IntegrityAlert[]> {
    return [...this.alerts];
  }

  private addAuditLog(actorRole: string, actorName: string, action: string, targetType: string, targetId: string, details: string) {
    this.auditLogs.unshift({
      id: `log_0${this.auditLogs.length + 1}`,
      timestamp: new Date().toISOString(),
      actorName,
      actorRole,
      action,
      targetType,
      targetId,
      details
    });
  }

  // CSV Export Mock
  exportCSV(type: string): string {
    if (type === 'results') {
      return `Rank,Project Title,Team Name,Track,Raw Score,Calibrated Score,Pairwise Win Rate\n1,Quiet Hours,Quantum Crafters,Developer Tools,9.15,9.38,92.5%\n2,Glass Signal,CyberForge Labs,AI Agents,8.85,8.92,85.0%\n3,Deep Compass,ZK Guild,Web3,8.40,8.55,78.0%`;
    }
    return `ID,Timestamp,Actor,Role,Action,Details\n1,2026-09-28 22:10:05,Dr. Ada Okonkwo,JUDGE,REVIEW_SUBMITTED,Submitted review score`;
  }
}

export const mockService = new MockService();
