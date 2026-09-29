import React from 'react';
import { UserRole } from '../mock/types';
import {
  LayoutDashboard, Users, Send, Grid, Gavel, GitCompare,
  BarChart3, ShieldAlert, Download, Settings, Layers, Trophy,
  Compass, UserCheck, Award, FileText, CheckCircle2, Sliders, Server
} from 'lucide-react';

interface SidebarProps {
  currentRole: UserRole;
  activeTab: string;
  onTabChange: (tab: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ currentRole, activeTab, onTabChange }) => {
  const getNavItems = () => {
    switch (currentRole) {
      case 'PARTICIPANT':
        return [
          { id: 'dashboard', label: 'Dashboard', icon: <LayoutDashboard className="w-4 h-4" /> },
          { id: 'explore', label: 'Explore Hackathons', icon: <Compass className="w-4 h-4" /> },
          { id: 'team', label: 'My Team', icon: <Users className="w-4 h-4" /> },
          { id: 'submit', label: 'Submit Project', icon: <Send className="w-4 h-4" /> },
          { id: 'submission_status', label: 'Submission Status', icon: <CheckCircle2 className="w-4 h-4" /> },
          { id: 'gallery', label: 'Project Gallery', icon: <Grid className="w-4 h-4" /> },
          { id: 'profile', label: 'Profile', icon: <UserCheck className="w-4 h-4" /> }
        ];

      case 'JUDGE':
        return [
          { id: 'judge_dashboard', label: 'Judge Dashboard', icon: <Gavel className="w-4 h-4" /> },
          { id: 'assignments', label: 'My Assignments', icon: <FileText className="w-4 h-4" /> },
          { id: 'pairwise', label: 'Pairwise Evaluation', icon: <GitCompare className="w-4 h-4" /> },
          { id: 'gallery', label: 'Project Gallery', icon: <Grid className="w-4 h-4" /> },
          { id: 'profile', label: 'Profile', icon: <UserCheck className="w-4 h-4" /> }
        ];

      case 'ORGANIZER':
        return [
          { id: 'org_dashboard', label: 'Event Overview', icon: <BarChart3 className="w-4 h-4" /> },
          { id: 'my_hackathons', label: 'My Hackathons', icon: <Compass className="w-4 h-4" /> },
          { id: 'participants_manage', label: 'Participants', icon: <UserCheck className="w-4 h-4" /> },
          { id: 'teams_manage', label: 'Teams', icon: <Users className="w-4 h-4" /> },
          { id: 'submissions_manage', label: 'Submissions', icon: <Send className="w-4 h-4" /> },
          { id: 'judging_manage', label: 'Judges & Workloads', icon: <Gavel className="w-4 h-4" /> },
          { id: 'rubric_manage', label: 'Rubric Config', icon: <Sliders className="w-4 h-4" /> },
          { id: 'results_manage', label: 'Leaderboard & Lifecycle', icon: <Trophy className="w-4 h-4" /> },
          { id: 'exports', label: 'CSV Export Center', icon: <Download className="w-4 h-4" /> },
          { id: 'audit_logs', label: 'Event Audit Trail', icon: <ShieldAlert className="w-4 h-4" /> }
        ];

      case 'ADMIN':
        return [
          { id: 'admin_dashboard', label: 'Platform Dashboard', icon: <Server className="w-4 h-4" /> },
          { id: 'admin_hackathons', label: 'All Hackathons', icon: <Compass className="w-4 h-4" /> },
          { id: 'admin_users', label: 'User Directory', icon: <Users className="w-4 h-4" /> },
          { id: 'admin_organizers', label: 'Organizers', icon: <BarChart3 className="w-4 h-4" /> },
          { id: 'admin_judges', label: 'Judges', icon: <Gavel className="w-4 h-4" /> },
          { id: 'admin_participants', label: 'Participants', icon: <Award className="w-4 h-4" /> },
          { id: 'admin_audit', label: 'Platform Audit Logs', icon: <ShieldAlert className="w-4 h-4" /> },
          { id: 'admin_settings', label: 'System Settings', icon: <Settings className="w-4 h-4" /> }
        ];

      default:
        return [];
    }
  };

  const navItems = getNavItems();

  return (
    <aside style={{
      width: 'var(--sidebar-width)',
      background: 'var(--bg-card)',
      borderRight: '1px solid var(--border-subtle)',
      padding: '1.25rem 0.875rem',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'space-between',
      height: 'calc(100vh - var(--navbar-height) - 45px)',
      position: 'sticky',
      top: 'calc(var(--navbar-height) + 45px)',
      overflowY: 'auto'
    }}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.25rem' }}>
        <div style={{ padding: '0 0.75rem 0.625rem 0.75rem', fontSize: '0.6875rem', fontWeight: 700, color: 'var(--text-muted)', letterSpacing: '0.05em' }}>
          {currentRole} PORTAL
        </div>
        {navItems.map((item) => {
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => onTabChange(item.id)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.75rem',
                padding: '0.625rem 1rem',
                borderRadius: '20px',
                fontSize: '0.875rem',
                fontWeight: isActive ? 600 : 500,
                color: isActive ? 'var(--google-blue-dark)' : 'var(--text-secondary)',
                background: isActive ? 'rgba(26, 115, 232, 0.12)' : 'transparent',
                border: 'none',
                cursor: 'pointer',
                textAlign: 'left',
                transition: 'all 0.15s ease'
              }}
            >
              <span style={{ color: isActive ? 'var(--google-blue-dark)' : 'var(--text-muted)' }}>{item.icon}</span>
              <span>{item.label}</span>
            </button>
          );
        })}
      </div>
    </aside>
  );
};
