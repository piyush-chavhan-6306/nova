import type { User } from './types';

export const DEMO_ACCOUNTS: Record<string, User> = {
  ADMIN: {
    id: 'usr_admin_001',
    name: 'Platform Administrator',
    email: 'admin@nova.dev',
    role: 'ADMIN',
    bio: 'Platform Root Operator & Global Systems Manager.',
    avatarUrl: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&auto=format&fit=crop&q=80'
  },
  ORGANIZER: {
    id: 'usr_org_001',
    name: 'Alex Organizer',
    email: 'organizer@nova.dev',
    role: 'ORGANIZER',
    bio: 'Lead Director for AI Innovation Challenge 2026.',
    avatarUrl: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80'
  },
  JUDGE: {
    id: 'usr_judge_001',
    name: 'Dr. Ada Okonkwo',
    email: 'judge@nova.dev',
    role: 'JUDGE',
    bio: 'Senior Principal Engineer & Hackathon Evaluator.',
    avatarUrl: 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=150&auto=format&fit=crop&q=80'
  },
  PARTICIPANT: {
    id: 'usr_participant_001',
    name: 'Priya Sharma',
    email: 'participant@nova.dev',
    role: 'PARTICIPANT',
    bio: 'Full-stack AI developer building open source Agentic systems.',
    avatarUrl: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80'
  }
};

export const MOCK_USERS: Record<string, User> = {
  ...DEMO_ACCOUNTS,
  // Fixture user aliases for mock compatibility
  'prt_01': DEMO_ACCOUNTS.PARTICIPANT,
  'jdg_01': DEMO_ACCOUNTS.JUDGE,
  'org_7f2a': DEMO_ACCOUNTS.ORGANIZER,
  'usr_admin': DEMO_ACCOUNTS.ADMIN
};
