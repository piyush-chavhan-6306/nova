import type { Team } from './types';

export const MOCK_TEAMS: Team[] = [
  {
    id: 'team_01',
    name: 'Quantum Crafters',
    hackathonId: 'evt_01',
    inviteCode: 'QC-2026-X9',
    members: [
      { userId: 'prt_01', name: 'Priya Participant', email: 'priya@dev.io', role: 'CAPTAIN' },
      { userId: 'prt_02', name: 'Marcus Chen', email: 'marcus@dev.io', role: 'MEMBER' },
      { userId: 'prt_03', name: 'Elena Rostova', email: 'elena@dev.io', role: 'MEMBER' }
    ]
  },
  {
    id: 'team_02',
    name: 'CyberForge Labs',
    hackathonId: 'evt_01',
    inviteCode: 'CF-8821-B4',
    members: [
      { userId: 'prt_04', name: 'Devon Vance', email: 'devon@cyber.io', role: 'CAPTAIN' },
      { userId: 'prt_05', name: 'Aisha Omar', email: 'aisha@cyber.io', role: 'MEMBER' }
    ]
  }
];
