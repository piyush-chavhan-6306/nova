import { apiClient } from './apiClient';

// ---- Hackathon types ----
export interface ApiHackathon {
  id: string;
  name: string;
  description?: string | null;
  registration_start?: string | null;
  registration_end?: string | null;
  submissions_start?: string | null;
  submissions_close?: string | null;
  status: string;
  min_team_size: number;
  max_team_size: number;
  payment_required: boolean;
  registration_fee: number;
  currency: string;
  blind_review_enabled: boolean;
  results_status: string;
  organizer_id?: string | null;
  created_at: string;
  tracks?: ApiTrack[];
  prizes?: ApiPrize[];
}

export interface ApiTrack {
  id: string;
  hackathon_id: string;
  name: string;
  description?: string | null;
}

export interface ApiPrize {
  id: string;
  hackathon_id: string;
  name: string;
  description?: string | null;
  value?: string | null;
}

export interface ApiRubricCriterion {
  id: string;
  rubric_id: string;
  name: string;
  weight: number;
  max_score: number;
  created_at: string;
}

export interface ApiRubric {
  id: string;
  hackathon_id: string;
  name: string;
  created_at: string;
  criteria?: ApiRubricCriterion[];
}

export interface ApiJudge {
  id: string;
  user_id: string;
  hackathon_id: string;
  title?: string | null;
  bio?: string | null;
  created_at: string;
}

export interface HackathonCreatePayload {
  name: string;
  description?: string;
  status?: string;
  registration_start?: string;
  registration_end?: string;
  submissions_start?: string;
  submissions_close?: string;
  max_team_size?: number;
  min_team_size?: number;
  blind_review_enabled?: boolean;
  payment_required?: boolean;
  registration_fee?: number;
  currency?: string;
}

export interface HackathonUpdatePayload extends Partial<HackathonCreatePayload> {}

// ---- Registration types ----
export interface ApiRegistration {
  id: string;
  hackathon_id: string;
  user_id: string;
  status: string;
  created_at: string;
}

// ---- Team types ----
export interface ApiTeamMember {
  id: string;
  team_id: string;
  user_id: string;
  role: string;
  user_name?: string | null;
  user_email?: string | null;
  joined_at: string;
}

export interface ApiTeam {
  id: string;
  hackathon_id: string;
  name: string;
  join_code?: string | null;
  created_at: string;
  members: ApiTeamMember[];
}

// ---- Submission types ----
export interface ApiSubmission {
  id: string;
  hackathon_id: string;
  team_id: string;
  track_id?: string | null;
  title: string;
  summary?: string | null;
  description?: string | null;
  repo_url?: string | null;
  demo_url?: string | null;
  status: string;
  submitted_at?: string | null;
  created_at: string;
  updated_at?: string | null;
}

export interface ApiGalleryProject {
  id: string;
  hackathon_id: string;
  team_id: string;
  track_id?: string | null;
  title: string;
  summary?: string | null;
  description?: string | null;
  repo_url?: string | null;
  demo_url?: string | null;
  status: string;
  team_name?: string | null;
  track_name?: string | null;
  submitted_at?: string | null;
}

// ---- Assignment/Review types ----
export interface ApiAssignment {
  id: string;
  judge_id: string;
  submission_id: string;
  status: string;
  assigned_at: string;
  completed_at?: string | null;
  assignment_round: number;
}

export interface ApiReview {
  id: string;
  assignment_id?: string | null;
  judge_id: string;
  submission_id: string;
  status: string;
  comment?: string | null;
  submitted_at?: string | null;
  created_at: string;
}

// ---- Leaderboard types ----
export interface ApiLeaderboardEntry {
  rank?: number;
  submission_id: string;
  team_id: string;
  title?: string;
  final_score?: number;
  track_id?: string;
}

export interface ApiLeaderboard {
  hackathon_id: string;
  status: string;
  entries: ApiLeaderboardEntry[];
}

// ===== SERVICE FUNCTIONS =====

export const hackathonService = {
  list: (params?: { search?: string; status?: string; skip?: number; limit?: number }) =>
    apiClient.get<ApiHackathon[]>('/hackathons', params as any),

  get: (id: string) =>
    apiClient.get<ApiHackathon>(`/hackathons/${id}`),

  create: (data: HackathonCreatePayload) =>
    apiClient.post<ApiHackathon>('/hackathons', data),

  update: (id: string, data: HackathonUpdatePayload) =>
    apiClient.put<ApiHackathon>(`/hackathons/${id}`, data),

  listTracks: (hackathonId: string) =>
    apiClient.get<ApiTrack[]>(`/hackathons/${hackathonId}/tracks`),

  createTrack: (hackathonId: string, data: { name: string; description?: string }) =>
    apiClient.post<ApiTrack>(`/hackathons/${hackathonId}/tracks`, data),

  listPrizes: (hackathonId: string) =>
    apiClient.get<ApiPrize[]>(`/hackathons/${hackathonId}/prizes`),

  createPrize: (hackathonId: string, data: { name: string; description?: string; value?: string }) =>
    apiClient.post<ApiPrize>(`/hackathons/${hackathonId}/prizes`, data),
    
  updatePrize: (hackathonId: string, prizeId: string, data: { name?: string; description?: string; value?: string }) =>
    apiClient.put<ApiPrize>(`/hackathons/${hackathonId}/prizes/${prizeId}`, data),

  deletePrize: (hackathonId: string, prizeId: string) =>
    apiClient.delete(`/hackathons/${hackathonId}/prizes/${prizeId}`),
};

export const registrationService = {
  register: (hackathonId: string) =>
    apiClient.post<ApiRegistration>('/registrations', { hackathon_id: hackathonId }),

  listForHackathon: (hackathonId: string) =>
    apiClient.get<ApiRegistration[]>(`/hackathons/${hackathonId}/registrations`),
};

export const teamService = {
  create: (hackathonId: string, name: string) =>
    apiClient.post<ApiTeam>('/teams', { hackathon_id: hackathonId, name }),

  get: (teamId: string) =>
    apiClient.get<ApiTeam>(`/teams/${teamId}`),

  listForHackathon: (hackathonId: string) =>
    apiClient.get<ApiTeam[]>(`/hackathons/${hackathonId}/teams`),

  invite: (teamId: string, email: string) =>
    apiClient.post(`/teams/${teamId}/invites`, { email }),

  removeMember: (teamId: string, userId: string) =>
    apiClient.delete(`/teams/${teamId}/members/${userId}`),
};

export const submissionService = {
  create: (data: {
    hackathon_id: string; team_id: string; title: string;
    track_id?: string; summary?: string; description?: string;
    repo_url?: string; demo_url?: string; is_draft?: boolean;
  }) => apiClient.post<ApiSubmission>('/submissions', data),

  update: (submissionId: string, data: {
    title?: string; track_id?: string; summary?: string;
    description?: string; repo_url?: string; demo_url?: string; is_draft?: boolean;
  }) => apiClient.put<ApiSubmission>(`/submissions/${submissionId}`, data),

  get: (submissionId: string) =>
    apiClient.get<ApiSubmission>(`/submissions/${submissionId}`),

  gallery: (params?: { hackathon_id?: string; skip?: number; limit?: number }) =>
    apiClient.get<ApiGalleryProject[]>('/gallery', params as any),
};

export const judgingService = {
  myAssignments: (hackathonId?: string) =>
    apiClient.get<ApiAssignment[]>('/judges/me/assignments', hackathonId ? { hackathon_id: hackathonId } : undefined),

  submitReview: (data: {
    submission_id: string; assignment_id?: string;
    comment?: string; scores?: { criterion_id: string; score: number; comment?: string }[];
  }) => apiClient.post<ApiReview>('/judging/reviews', data),

  getReviewsForSubmission: (submissionId: string) =>
    apiClient.get<ApiReview[]>(`/judging/submissions/${submissionId}/reviews`),
};

export const resultsService = {
  get: (hackathonId: string) =>
    apiClient.get<ApiLeaderboard>(`/hackathons/${hackathonId}/results`),

  calculate: (hackathonId: string) =>
    apiClient.post<ApiLeaderboard>(`/hackathons/${hackathonId}/results/calculate`),

  publish: (hackathonId: string) =>
    apiClient.post<ApiLeaderboard>(`/hackathons/${hackathonId}/results/publish`),

  lock: (hackathonId: string) =>
    apiClient.post<ApiLeaderboard>(`/hackathons/${hackathonId}/results/lock`),
};

export const organizerService = {
  dashboard: (hackathonId: string) =>
    apiClient.get(`/hackathons/${hackathonId}/organizer/dashboard`),

  submissionAnalytics: (hackathonId: string) =>
    apiClient.get(`/hackathons/${hackathonId}/analytics/submissions`),

  integrityChecks: (hackathonId: string) =>
    apiClient.get(`/hackathons/${hackathonId}/integrity/checks`),

  exportResultsCsv: (hackathonId: string) =>
    apiClient.downloadCsv(`/hackathons/${hackathonId}/exports/results.csv`),

  exportJudgingCsv: (hackathonId: string) =>
    apiClient.downloadCsv(`/hackathons/${hackathonId}/exports/judging.csv`),

  exportJudgesCsv: (hackathonId: string) =>
    apiClient.downloadCsv(`/hackathons/${hackathonId}/exports/judges.csv`),
};

export const rubricService = {
  list: (hackathonId: string) =>
    apiClient.get<ApiRubric[]>(`/hackathons/${hackathonId}/rubrics`),

  get: (rubricId: string) =>
    apiClient.get<ApiRubric>(`/rubrics/${rubricId}`),

  create: (hackathonId: string, name: string) =>
    apiClient.post<ApiRubric>(`/hackathons/${hackathonId}/rubrics`, { name }),

  update: (rubricId: string, name: string) =>
    apiClient.put<ApiRubric>(`/rubrics/${rubricId}`, { name }),

  delete: (rubricId: string) =>
    apiClient.delete(`/rubrics/${rubricId}`),

  addCriterion: (rubricId: string, data: { name: string; weight?: number; max_score?: number }) =>
    apiClient.post<ApiRubricCriterion>(`/rubrics/${rubricId}/criteria`, data),

  updateCriterion: (criterionId: string, data: { name?: string; weight?: number; max_score?: number }) =>
    apiClient.put<ApiRubricCriterion>(`/rubric-criteria/${criterionId}`, data),

  deleteCriterion: (criterionId: string) =>
    apiClient.delete(`/rubric-criteria/${criterionId}`),
};

export const judgeManagementService = {
  list: (hackathonId: string) =>
    apiClient.get<ApiJudge[]>(`/hackathons/${hackathonId}/judges`),

  invite: (hackathonId: string, userId: string, title?: string, bio?: string) =>
    apiClient.post<ApiJudge>(`/hackathons/${hackathonId}/judges`, { user_id: userId, title, bio }),

  update: (judgeId: string, title?: string, bio?: string) =>
    apiClient.put<ApiJudge>(`/judges/${judgeId}`, { title, bio }),

  delete: (judgeId: string) =>
    apiClient.delete(`/judges/${judgeId}`),

  assignTrack: (judgeId: string, trackId: string) =>
    apiClient.post(`/judges/${judgeId}/tracks`, { track_id: trackId }),

  removeTrack: (judgeId: string, trackId: string) =>
    apiClient.delete(`/judges/${judgeId}/tracks/${trackId}`),
};

export const auditService = {
  getLogs: (hackathonId?: string, limit?: number) =>
    apiClient.get<any[]>('/audit-logs', { hackathon_id: hackathonId, limit: limit || 100 } as any),
};
