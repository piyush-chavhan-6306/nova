import React, { useState, useEffect } from 'react';
import { UserRole, User, Hackathon, Submission, Team, JudgeAssignment, LeaderboardResult, AuditLogItem, IntegrityAlert } from './mock/types';
import { mockService } from './services/mockService';
import { authService } from './services/authService';
import { RoleSwitcher } from './components/RoleSwitcher';
import { Navbar } from './components/Navbar';
import { Sidebar } from './components/Sidebar';
import { Toast, ToastMessage } from './components/Toast';
import { SubmissionWizard } from './components/SubmissionWizard';

import { LoginPage } from './pages/LoginPage';
import { ParticipantDashboard } from './pages/ParticipantDashboard';
import { ExploreHackathons } from './pages/ExploreHackathons';
import { HackathonDetailsPage } from './pages/HackathonDetailsPage';
import { TeamManagement } from './pages/TeamManagement';
import { SubmissionStatusPage } from './pages/SubmissionStatusPage';
import { ProjectGallery } from './pages/ProjectGallery';

import { JudgeDashboard } from './pages/JudgeDashboard';
import { JudgeAssignmentsPage } from './pages/JudgeAssignmentsPage';
import { PairwiseJudging } from './pages/PairwiseJudging';

import { OrganizerDashboard } from './pages/OrganizerDashboard';
import { OrganizerHackathonsPage } from './pages/OrganizerHackathonsPage';
import {
  OrganizerParticipantsPage,
  OrganizerTeamsPage,
  OrganizerSubmissionsPage,
  OrganizerJudgesPage,
  OrganizerRubricPage,
  OrganizerResultsPage,
  OrganizerExportsPage,
  OrganizerAuditPage
} from './pages/OrganizerPages';

import { AdminDashboard } from './pages/AdminDashboard';
import { AdminUsersPage } from './pages/AdminUsersPage';
import {
  AdminHackathonsPage,
  AdminOrganizersPage,
  AdminJudgesPage,
  AdminParticipantsPage,
  AdminAuditPage,
  AdminSettingsPage
} from './pages/AdminPages';

import { CheckCircle2, Users } from 'lucide-react';
import { ParticipantProfilePage, JudgeProfilePage } from './pages/UserProfilePages';

import { useAuth, AuthUser } from './context/AuthContext';
import { hackathonService, registrationService, teamService, submissionService, judgingService, resultsService, organizerService } from './services/api/novaApi';

export function App() {
  const { user: authUser, logout, login, isLoading: authLoading } = useAuth();

  const currentUser: User | null = authUser ? {
    id: authUser.id,
    name: authUser.name,
    email: authUser.email,
    role: authUser.role as UserRole,
    avatarUrl: authUser.avatarUrl || authUser.avatar_url || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80',
    bio: authUser.bio || undefined,
  } : null;
  const [activeTab, setActiveTab] = useState<string>('dashboard');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [activeHackathonId, setActiveHackathonId] = useState<string>('evt_01');

  const [hackathon, setHackathon] = useState<Hackathon | null>(null);
  const [allHackathons, setAllHackathons] = useState<Hackathon[]>([]);
  const [selectedHackathon, setSelectedHackathon] = useState<Hackathon | null>(null);
  const [submissions, setSubmissions] = useState<Submission[]>([]);
  const [teams, setTeams] = useState<Team[]>([]);
  const [assignments, setAssignments] = useState<JudgeAssignment[]>([]);
  const [leaderboard, setLeaderboard] = useState<LeaderboardResult[]>([]);
  const [auditLogs, setAuditLogs] = useState<AuditLogItem[]>([]);
  const [alerts, setAlerts] = useState<IntegrityAlert[]>([]);
  const [allUsers, setAllUsers] = useState<User[]>([]);
  const [adminStats, setAdminStats] = useState<any>({ totalHackathons: 4, activeHackathons: 2, totalParticipants: 142, totalOrganizers: 8, totalJudges: 12, totalSubmissions: 38 });

  const [isWizardOpen, setIsWizardOpen] = useState<boolean>(false);
  const [selectedEvaluationSubmissionId, setSelectedEvaluationSubmissionId] = useState<string | null>(null);
  const [toasts, setToasts] = useState<ToastMessage[]>([]);

  // Registration & Team state for Participant Journey
  const [registeredHackathonIds, setRegisteredHackathonIds] = useState<string[]>(['h1']);
  const [registeredSuccessHackathon, setRegisteredSuccessHackathon] = useState<Hackathon | null>(null);

  useEffect(() => {
    loadData();
  }, [currentUser?.role]);

  const loadData = async () => {
    // 1. Fetch from Real API
    let allH: Hackathon[] = [];
    try {
      const apiHacks = await hackathonService.list();
      allH = await Promise.all(apiHacks.map(async (apiH) => {
        let tracks: any[] = [];
        try {
          tracks = await hackathonService.listTracks(apiH.id);
        } catch (e) {
          tracks = [];
        }
        return {
          id: apiH.id,
          name: apiH.name,
          tagline: '', // Unsupported by backend
          description: apiH.description || '',
          status: apiH.status as any,
          submissionsClose: apiH.submissions_close || '',
          blindReviewEnabled: apiH.blind_review_enabled || false,
          resultsStatus: apiH.results_status as any,
          tracks: tracks.map(t => ({ id: t.id, name: t.name, description: t.description || '' })),
          rubric: [], // Unsupported by backend 
          organizerId: apiH.organizer_id || '',
          participantCount: 0,
          prizePool: '', // Unsupported by backend 
        };
      }));
    } catch {
      allH = await mockService.getHackathons();
    }
    
    // Set currently active hackathon context (if none selected, default to the first one)
    const h = allH.length > 0 ? allH[0] : await mockService.getHackathon();

    const subs = await mockService.getSubmissions();
    const t = await mockService.getTeams();
    const asg = await mockService.getJudgeAssignments(currentUser?.id || 'usr_judge_001');
    const lb = await mockService.getLeaderboard();
    const logs = await mockService.getAuditLogs();
    const alt = await mockService.getIntegrityAlerts();
    const uList = await mockService.getAllUsers();
    const stats = await mockService.getAdminStats();

    setHackathon(h);
    setAllHackathons(allH);
    setSubmissions(subs);
    setTeams(t);
    setAssignments(asg);
    setLeaderboard(lb);
    setAuditLogs(logs);
    setAlerts(alt);
    setAllUsers(uList);
    setAdminStats(stats);
  };

  const addToast = (type: 'success' | 'warning' | 'error' | 'info', message: string) => {
    const newToast: ToastMessage = { id: `t_${Date.now()}`, type, message };
    setToasts(prev => [...prev, newToast]);
    setTimeout(() => {
      setToasts(prev => prev.filter(t => t.id !== newToast.id));
    }, 4000);
  };

  const currentHackathonId = selectedHackathon?.id || activeHackathonId || hackathon?.id || 'evt_01';
  const getTeamForHackathon = (targetHackathonId: string): Team | null => {
    if (!targetHackathonId) return null;
    const matchingTeam = teams.find(t => 
      (t.hackathonId === targetHackathonId || (t as any).hackathon_id === targetHackathonId) && 
      t.members.some(m => m.userId === currentUser?.id || m.email === currentUser?.email || (m as any).user_id === currentUser?.id || (m as any).user_email === currentUser?.email)
    );
    if (matchingTeam) return matchingTeam;

    if (currentUser) {
      try {
        const stored = localStorage.getItem(`nova_team_${currentUser.id}_${targetHackathonId}`);
        if (stored) {
          return JSON.parse(stored);
        }
      } catch (e) {}
    }
    return null;
  };

  const currentTeam = getTeamForHackathon(currentHackathonId);

  const handleRegisterHackathon = (h: Hackathon) => {
    if (!registeredHackathonIds.includes(h.id)) {
      setRegisteredHackathonIds(prev => [...prev, h.id]);
    }
    setRegisteredSuccessHackathon(h);
    setActiveHackathonId(h.id);
    addToast('success', `Successfully registered for ${h.name}!`);
  };

  const handleCreateTeam = async (teamName: string) => {
    const targetHackathonId = currentHackathonId;
    let createdTeam: Team;
    try {
      const apiTeam = await teamService.create(targetHackathonId, teamName);
      createdTeam = {
        id: apiTeam.id,
        name: apiTeam.name,
        hackathonId: apiTeam.hackathon_id,
        inviteCode: apiTeam.join_code || `INV-${Date.now()}`,
        members: apiTeam.members.map(m => ({
          userId: m.user_id,
          name: m.user_name || currentUser?.name || 'Jane Cooper',
          email: m.user_email || currentUser?.email || 'participant@nova.dev',
          role: m.role === 'LEAD' ? 'CAPTAIN' : 'MEMBER'
        }))
      };
    } catch (err) {
      createdTeam = {
        id: `team_${Date.now()}`,
        hackathonId: targetHackathonId,
        name: teamName,
        inviteCode: `${teamName.substring(0, 3).toUpperCase()}-2026-${Math.floor(10 + Math.random() * 89)}`,
        members: [
          {
            userId: currentUser?.id || 'usr_part_001',
            name: currentUser?.name || 'Jane Cooper',
            email: currentUser?.email || 'participant@nova.dev',
            role: 'CAPTAIN'
          }
        ]
      };
    }
    
    setTeams(prev => [createdTeam, ...prev.filter(t => t.id !== createdTeam.id)]);
    if (currentUser) {
      localStorage.setItem(`nova_team_${currentUser.id}_${targetHackathonId}`, JSON.stringify(createdTeam));
    }
    addToast('success', `Created team "${teamName}" with invite code ${createdTeam.inviteCode}!`);
  };

  const handleJoinTeam = (inviteCode: string) => {
    const targetHackathonId = currentHackathonId;
    const newTeam: Team = {
      id: `team_${Date.now()}`,
      hackathonId: targetHackathonId,
      name: 'Joined Team',
      inviteCode: inviteCode.toUpperCase(),
      members: [
        {
          userId: currentUser?.id || 'usr_part_001',
          name: currentUser?.name || 'Jane Cooper',
          email: currentUser?.email || 'participant@nova.dev',
          role: 'MEMBER'
        }
      ]
    };
    setTeams(prev => [newTeam, ...prev]);
    if (currentUser) {
      localStorage.setItem(`nova_team_${currentUser.id}_${targetHackathonId}`, JSON.stringify(newTeam));
    }
    addToast('success', `Joined team with code ${inviteCode}!`);
  };

  const handleLoginSuccess = (u: AuthUser) => {
    if (u.role === 'ADMIN') setActiveTab('admin_dashboard');
    else if (u.role === 'ORGANIZER') setActiveTab('org_dashboard');
    else if (u.role === 'JUDGE') setActiveTab('judge_dashboard');
    else setActiveTab('dashboard');
    addToast('success', `Welcome back, ${u.name}! Logged in as ${u.role}.`);
  };

  const handleLogout = () => {
    logout();
    addToast('info', 'Logged out of session.');
  };

  const handleRoleChange = async (role: UserRole) => {
    const roleEmailMap: Record<UserRole, string> = {
      ADMIN: 'admin@nova.dev',
      ORGANIZER: 'organizer@nova.dev',
      JUDGE: 'judge@nova.dev',
      PARTICIPANT: 'participant@nova.dev',
    };
    const targetEmail = roleEmailMap[role];
    if (targetEmail) {
      try {
        const u = await login(targetEmail, 'nova2026!');
        if (role === 'PARTICIPANT') setActiveTab('dashboard');
        else if (role === 'JUDGE') setActiveTab('judge_dashboard');
        else if (role === 'ORGANIZER') setActiveTab('org_dashboard');
        else if (role === 'ADMIN') setActiveTab('admin_dashboard');
        addToast('info', `Switched authenticated session to ${u.name} (${u.role})`);
      } catch (err: any) {
        addToast('error', `Failed to switch role: ${err?.detail || err?.message}`);
      }
    }
  };

  const handleSaveSubmission = async (subData: Partial<Submission>) => {
    try {
      if (subData.title) {
        await submissionService.create({
          hackathon_id: subData.hackathonId || currentHackathonId,
          team_id: subData.teamId || currentTeam?.id || 'team_01',
          title: subData.title,
          track_id: subData.trackId,
          summary: subData.summary,
          description: subData.description,
          repo_url: subData.repoUrl,
          demo_url: subData.demoUrl,
          is_draft: subData.status === 'DRAFT',
        });
      }
    } catch {
      await mockService.createOrUpdateSubmission(subData);
    }
    await loadData();
    addToast('success', 'Project submission saved and locked for blind review!');
  };

  const handleAddTeamMember = async (email: string, name: string) => {
    if (currentTeam) {
      try {
        await teamService.invite(currentTeam.id, email);
      } catch {
        await mockService.addTeamMember(currentTeam.id, email, name);
      }
      await loadData();
      addToast('success', `Invited ${name} (${email}) to team!`);
    }
  };

  const handleCreateHackathon = async (data: Partial<Hackathon>) => {
    try {
      if (data.name) {
        await hackathonService.create({
          name: data.name,
          description: data.description || '',
          status: data.status || 'ACTIVE',
          blind_review_enabled: data.blindReviewEnabled ?? true,
        });
      }
    } catch {
      await mockService.createHackathon(data, currentUser?.id || 'usr_org_001');
    }
    await loadData();
    addToast('success', `Created new hackathon event: ${data.name}!`);
  };

  const handleUpdateHackathon = async (id: string, data: Partial<Hackathon>) => {
    try {
      await hackathonService.update(id, {
        name: data.name,
        description: data.description,
        status: data.status,
        blind_review_enabled: data.blindReviewEnabled,
      });
    } catch {
      await mockService.updateHackathon(id, data);
    }
    await loadData();
    addToast('success', `Updated hackathon information for ${data.name || 'event'}!`);
  };

  const handleSaveReview = async (submissionId: string, scores: any[], comment: string, isSubmit: boolean) => {
    try {
      await judgingService.submitReview({
        submission_id: submissionId,
        comment,
        scores: scores.map(s => ({ criterion_id: s.criterionId, score: s.score, comment: s.comment }))
      });
    } catch {
      await mockService.saveReview(submissionId, currentUser?.id || 'usr_judge_001', scores, comment, isSubmit);
    }
    await loadData();
    addToast('success', isSubmit ? 'Submitted review score!' : 'Saved review draft');
  };

  const handleSubmitPairwise = async (evalId: string, winnerId: string, reason: string) => {
    await mockService.submitPairwiseDecision(evalId, winnerId, reason);
    await loadData();
    addToast('success', 'Submitted pairwise decision winner!');
  };

  const handleToggleBlindReview = async () => {
    const newState = await mockService.toggleBlindReview();
    await loadData();
    addToast('warning', `Blind Review mode set to ${newState ? 'ACTIVE' : 'INACTIVE'}`);
  };

  const handleUpdateResultsStatus = async (status: Hackathon['resultsStatus']) => {
    try {
      if (status === 'CALCULATED') {
        await resultsService.calculate('evt_01');
      } else if (status === 'PUBLISHED') {
        await resultsService.publish('evt_01');
      } else if (status === 'LOCKED') {
        await resultsService.lock('evt_01');
      }
    } catch {
      await mockService.updateResultsStatus(status);
    }
    await loadData();
    addToast('info', `Results lifecycle state set to ${status}`);
  };

  const handleExportCSV = async (type: string) => {
    try {
      let downloadUrl = '';
      if (type === 'results') {
        downloadUrl = await organizerService.exportResultsCsv('evt_01');
      } else if (type === 'judging') {
        downloadUrl = await organizerService.exportJudgingCsv('evt_01');
      } else if (type === 'judges') {
        downloadUrl = await organizerService.exportJudgesCsv('evt_01');
      }
      if (downloadUrl) {
        const a = document.createElement('a');
        a.href = downloadUrl;
        a.download = `nova_${type}_export.csv`;
        a.click();
        addToast('success', `Downloaded real backend ${type} CSV export!`);
        return;
      }
    } catch {
      // fallback
    }
    const csvData = mockService.exportCSV(type);
    const blob = new Blob([csvData], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `nova_${type}_export.csv`;
    a.click();
    addToast('success', `Downloaded ${type} CSV export!`);
  };

  if (authLoading) {
    return (
      <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#202124', color: '#fff' }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '1.25rem', fontWeight: 600, marginBottom: '0.5rem' }}>Loading NOVA Portal...</div>
          <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>Validating session with backend</div>
        </div>
      </div>
    );
  }

  // 1. Unauthenticated -> Show Unified Login Screen
  if (!currentUser) {
    return <LoginPage onLoginSuccess={handleLoginSuccess} />;
  }

  if (!hackathon) return null;

  return (
    <div style={{ minHeight: '100vh', background: 'var(--bg-dark)', color: 'var(--text-primary)' }}>
      {/* Top Demo Role Switcher Toolbar */}
      <RoleSwitcher
        currentRole={currentUser.role}
        currentUser={currentUser}
        onRoleChange={handleRoleChange}
        onLogout={handleLogout}
      />

      {/* Main Header */}
      <Navbar
        hackathon={selectedHackathon || hackathon}
        searchQuery={searchQuery}
        onSearchChange={setSearchQuery}
      />

      <div style={{ display: 'flex' }}>
        {/* Left Role-Specific Sidebar */}
        <Sidebar
          currentRole={currentUser.role}
          activeTab={activeTab}
          onTabChange={(tab) => {
            setSelectedHackathon(null);
            setActiveTab(tab);
          }}
        />

        {/* Main Content Viewport */}
        <main style={{ flex: 1, padding: '2rem 2.5rem', maxWidth: '1400px' }}>

          {/* PARTICIPANT PORTAL VIEWS */}
          {currentUser.role === 'PARTICIPANT' && (
            <>
              {selectedHackathon ? (
                <HackathonDetailsPage
                  hackathon={selectedHackathon}
                  isRegistered={registeredHackathonIds.includes(selectedHackathon.id)}
                  hasTeam={Boolean(getTeamForHackathon(selectedHackathon.id))}
                  onBack={() => setSelectedHackathon(null)}
                  onOpenSubmitWizard={() => setIsWizardOpen(true)}
                  onRegister={() => handleRegisterHackathon(selectedHackathon)}
                  onGoToTeam={() => {
                    setActiveHackathonId(selectedHackathon.id);
                    setSelectedHackathon(null);
                    setActiveTab('team');
                  }}
                />
              ) : (
                <>
                  {activeTab === 'dashboard' && (
                    <ParticipantDashboard
                      submissions={submissions.filter(s => s.hackathonId === currentHackathonId)}
                      team={currentTeam || undefined}
                      onOpenWizard={() => setIsWizardOpen(true)}
                    />
                  )}

                  {activeTab === 'explore' && (
                    <ExploreHackathons
                      onSelectHackathon={(h) => {
                        setSelectedHackathon(h);
                        setActiveHackathonId(h.id);
                      }}
                    />
                  )}

                  {activeTab === 'team' && (
                    <TeamManagement
                      team={currentTeam || null}
                      hackathonName={allHackathons.find(h => h.id === currentHackathonId)?.name || hackathon?.name}
                      onAddMember={handleAddTeamMember}
                      onCreateTeam={handleCreateTeam}
                      onJoinTeam={handleJoinTeam}
                      onOpenSubmitWizard={() => setIsWizardOpen(true)}
                    />
                  )}

                  {activeTab === 'submit' && (
                    <ParticipantDashboard
                      submissions={submissions.filter(s => s.hackathonId === currentHackathonId)}
                      team={currentTeam || undefined}
                      onOpenWizard={() => setIsWizardOpen(true)}
                    />
                  )}

                  {activeTab === 'submission_status' && (
                    <SubmissionStatusPage
                      submission={submissions[0]}
                      onOpenWizard={() => setIsWizardOpen(true)}
                    />
                  )}

                  {activeTab === 'gallery' && (
                    <ProjectGallery
                      submissions={submissions}
                      tracks={hackathon.tracks}
                      searchQuery={searchQuery}
                    />
                  )}

                  {activeTab === 'profile' && (
                    <ParticipantProfilePage user={currentUser} />
                  )}
                </>
              )}
            </>
          )}

          {/* JUDGE PORTAL VIEWS */}
          {currentUser.role === 'JUDGE' && (
            <>
              {activeTab === 'judge_dashboard' && (
                <JudgeDashboard
                  assignments={assignments}
                  submissions={submissions}
                  hackathon={hackathon}
                  onSaveReview={handleSaveReview}
                />
              )}

              {activeTab === 'assignments' && (
                <JudgeAssignmentsPage
                  assignments={assignments}
                  submissions={submissions}
                  hackathon={hackathon}
                  onOpenEvaluation={(subId) => setSelectedEvaluationSubmissionId(subId)}
                />
              )}

              {activeTab === 'pairwise' && (
                <PairwiseJudging
                  evaluations={awaitingPairwiseEvaluations()}
                  submissions={submissions}
                  onSubmitDecision={handleSubmitPairwise}
                />
              )}

              {activeTab === 'gallery' && (
                <ProjectGallery
                  submissions={submissions}
                  tracks={hackathon.tracks}
                  searchQuery={searchQuery}
                />
              )}

              {activeTab === 'profile' && (
                <JudgeProfilePage user={currentUser} />
              )}
            </>
          )}

          {/* ORGANIZER PORTAL VIEWS */}
          {currentUser.role === 'ORGANIZER' && (
            <>
              {activeTab === 'org_dashboard' && (
                <OrganizerDashboard
                  hackathon={hackathon}
                  submissions={submissions}
                  leaderboard={leaderboard}
                  auditLogs={auditLogs}
                  alerts={alerts}
                  onToggleBlindReview={handleToggleBlindReview}
                  onUpdateResultsStatus={handleUpdateResultsStatus}
                  onExportCSV={handleExportCSV}
                />
              )}

              {activeTab === 'my_hackathons' && (
                <OrganizerHackathonsPage
                  hackathons={allHackathons}
                  currentUser={currentUser}
                  onCreateHackathon={handleCreateHackathon}
                  onUpdateHackathon={handleUpdateHackathon}
                  onSelectHackathon={(h) => {
                    setHackathon(h);
                    setActiveTab('org_dashboard');
                    addToast('info', `Switched active command center to ${h.name}`);
                  }}
                />
              )}

              {activeTab === 'participants_manage' && (
                <OrganizerParticipantsPage hackathon={hackathon} />
              )}

              {activeTab === 'teams_manage' && (
                <OrganizerTeamsPage />
              )}

              {activeTab === 'submissions_manage' && (
                <OrganizerSubmissionsPage submissions={submissions} />
              )}

              {activeTab === 'judging_manage' && (
                <OrganizerJudgesPage />
              )}

              {activeTab === 'rubric_manage' && (
                <OrganizerRubricPage hackathon={hackathon} />
              )}

              {activeTab === 'results_manage' && (
                <OrganizerResultsPage
                  leaderboard={leaderboard}
                  hackathon={hackathon}
                  onUpdateResultsStatus={handleUpdateResultsStatus}
                />
              )}

              {activeTab === 'exports' && (
                <OrganizerExportsPage onExportCSV={handleExportCSV} />
              )}

              {activeTab === 'audit_logs' && (
                <OrganizerAuditPage auditLogs={auditLogs} alerts={alerts} />
              )}
            </>
          )}

          {/* ADMIN PORTAL VIEWS */}
          {currentUser.role === 'ADMIN' && (
            <>
              {activeTab === 'admin_dashboard' && (
                <AdminDashboard
                  stats={adminStats}
                  hackathons={allHackathons}
                  users={allUsers}
                  auditLogs={auditLogs}
                />
              )}

              {activeTab === 'admin_hackathons' && (
                <AdminHackathonsPage hackathons={allHackathons} />
              )}

              {activeTab === 'admin_users' && (
                <AdminUsersPage users={allUsers} />
              )}

              {activeTab === 'admin_organizers' && (
                <AdminOrganizersPage users={allUsers} hackathons={allHackathons} />
              )}

              {activeTab === 'admin_judges' && (
                <AdminJudgesPage users={allUsers} />
              )}

              {activeTab === 'admin_participants' && (
                <AdminParticipantsPage users={allUsers} />
              )}

              {activeTab === 'admin_audit' && (
                <AdminAuditPage auditLogs={auditLogs} />
              )}

              {activeTab === 'admin_settings' && (
                <AdminSettingsPage />
              )}
            </>
          )}

        </main>
      </div>

      {/* Submission Wizard Modal */}
      {isWizardOpen && (
        <SubmissionWizard
          initialSubmission={submissions[0]}
          onSave={handleSaveSubmission}
          onClose={() => setIsWizardOpen(false)}
        />
      )}

      {/* Registration Success Modal */}
      {registeredSuccessHackathon && (
        <div style={{ position: 'fixed', inset: 0, zIndex: 250, background: 'rgba(0,0,0,0.85)', backdropFilter: 'blur(12px)', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '1rem' }}>
          <div className="glass-panel animate-fade-in" style={{ width: '100%', maxWidth: '520px', padding: '2rem', borderRadius: '20px', textAlign: 'center' }}>
            <div style={{ width: '64px', height: '64px', borderRadius: '50%', background: 'rgba(16, 185, 129, 0.15)', color: '#10b981', border: '1px solid rgba(16, 185, 129, 0.3)', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 1.25rem auto' }}>
              <CheckCircle2 className="w-8 h-8" />
            </div>
            <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--text-primary)', marginBottom: '0.5rem' }}>
              Registration Confirmed!
            </h2>
            <p style={{ fontSize: '0.9375rem', color: 'var(--text-secondary)', marginBottom: '1.5rem', lineHeight: 1.5 }}>
              You are now registered for <strong>{registeredSuccessHackathon.name}</strong>. Next, set up your team to unlock project submissions.
            </p>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              <button
                onClick={() => {
                  setRegisteredSuccessHackathon(null);
                  setSelectedHackathon(null);
                  setActiveTab('team');
                }}
                className="btn btn-primary"
                style={{ padding: '0.875rem' }}
              >
                <Users className="w-4 h-4" />
                <span>Go to Team Formation (Create / Join Team)</span>
              </button>

              <button
                onClick={() => setRegisteredSuccessHackathon(null)}
                className="btn btn-secondary"
                style={{ padding: '0.625rem' }}
              >
                <span>Continue Exploring Hackathon</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Interactive Toast Notifications */}
      <Toast toasts={toasts} onDismiss={(id) => setToasts(prev => prev.filter(t => t.id !== id))} />
    </div>
  );

  function awaitingPairwiseEvaluations() {
    return [
      {
        id: 'pw_01',
        judgeId: currentUser?.id || 'usr_judge_001',
        submissionAId: 'prj_01',
        submissionATitle: 'Quiet Hours',
        submissionBId: 'prj_02',
        submissionBTitle: 'Glass Signal',
        winnerSubmissionId: 'prj_01',
        reason: 'Quiet Hours demonstrated higher architectural maturity.',
        status: 'SUBMITTED' as const
      }
    ];
  }
}

export default App;
