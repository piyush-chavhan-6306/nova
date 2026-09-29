import type { Hackathon } from './types';

export const MOCK_HACKATHONS: Hackathon[] = [
  {
    id: 'evt_01',
    name: 'AI Innovation Challenge 2026',
    tagline: 'Building Next-Generation Autonomous Developer Tools & LLM Agents',
    status: 'ACTIVE',
    submissionsClose: '2026-10-15T23:59:59Z',
    blindReviewEnabled: true,
    resultsStatus: 'UNDER_REVIEW',
    organizerId: 'usr_org_001',
    organizerName: 'Alex Organizer',
    bannerUrl: 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=800&auto=format&fit=crop&q=80',
    prizePool: '$50,000 USD',
    participantCount: 142,
    teamCount: 38,
    submissionCount: 38,
    tracks: [
      {
        id: 'trk_01',
        name: 'Developer Tools & Automation',
        description: 'CLIs, compilers, IDE plugins, CI/CD runners, and workflow automations.'
      },
      {
        id: 'trk_02',
        name: 'Artificial Intelligence & Agents',
        description: 'LLM agents, autonomous coding assistants, and local AI models.'
      },
      {
        id: 'trk_03',
        name: 'Web3 & Decentralized Infrastructure',
        description: 'Distributed storage, peer-to-peer protocols, and cryptographic verification.'
      }
    ],
    rubric: [
      {
        id: 'rub_01',
        name: 'Functionality & Architecture',
        maxScore: 10,
        weight: 0.35,
        description: 'Does the software work reliably? Is the code architecture scalable?'
      },
      {
        id: 'rub_02',
        name: 'User Experience & Interface',
        maxScore: 10,
        weight: 0.25,
        description: 'Is the UI responsive, polished, intuitive, and accessible?'
      },
      {
        id: 'rub_03',
        name: 'Technical Originality',
        maxScore: 10,
        weight: 0.25,
        description: 'How innovative is the technical approach and problem-solving method?'
      },
      {
        id: 'rub_04',
        name: 'Presentation & Pitch',
        maxScore: 10,
        weight: 0.15,
        description: 'Is the project summary, documentation, and video demo clear and compelling?'
      }
    ]
  },
  {
    id: 'evt_02',
    name: 'Quantum & Security Hackathon 2026',
    tagline: 'Post-Quantum Cryptography & Zero-Trust System Defense',
    status: 'ACTIVE',
    submissionsClose: '2026-11-01T23:59:59Z',
    blindReviewEnabled: false,
    resultsStatus: 'DRAFT',
    organizerId: 'usr_org_001',
    organizerName: 'Alex Organizer',
    bannerUrl: 'https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800&auto=format&fit=crop&q=80',
    prizePool: '$35,000 USD',
    participantCount: 88,
    teamCount: 22,
    submissionCount: 18,
    tracks: [
      { id: 'trk_sec_01', name: 'Post-Quantum Crypto', description: 'NIST PQ algorithm implementations and benchmarks.' },
      { id: 'trk_sec_02', name: 'Zero-Trust Networks', description: 'Distributed identity & access verification engines.' }
    ],
    rubric: [
      { id: 'rub_sec_01', name: 'Security Rigor', maxScore: 10, weight: 0.5, description: 'Correctness of security logic and attack mitigation.' },
      { id: 'rub_sec_02', name: 'Performance', maxScore: 10, weight: 0.5, description: 'Throughput and latency overhead benchmarks.' }
    ]
  },
  {
    id: 'evt_03',
    name: 'Web3 Infrastructure World 2026',
    tagline: 'High-Throughput L2 Rollups & Decentralized Cloud',
    status: 'UPCOMING',
    submissionsClose: '2026-12-15T23:59:59Z',
    blindReviewEnabled: true,
    resultsStatus: 'DRAFT',
    organizerId: 'usr_org_002',
    organizerName: 'Elena Rostova',
    bannerUrl: 'https://images.unsplash.com/photo-1639762681485-074b7f938ba0?w=800&auto=format&fit=crop&q=80',
    prizePool: '$75,000 USD',
    participantCount: 210,
    teamCount: 54,
    submissionCount: 0,
    tracks: [
      { id: 'trk_w3_01', name: 'Zero-Knowledge Proofs', description: 'zk-SNARKs and zk-STARK prover optimization.' }
    ],
    rubric: [
      { id: 'rub_w3_01', name: 'Scalability', maxScore: 10, weight: 1.0, description: 'Transactions per second scaling efficiency.' }
    ]
  },
  {
    id: 'evt_04',
    name: 'Global DevTools Code Jam 2025',
    tagline: 'Developer Productivity & Code Intelligence Tools',
    status: 'CLOSED',
    submissionsClose: '2025-12-01T23:59:59Z',
    blindReviewEnabled: true,
    resultsStatus: 'PUBLISHED',
    organizerId: 'usr_org_002',
    organizerName: 'Elena Rostova',
    bannerUrl: 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&auto=format&fit=crop&q=80',
    prizePool: '$25,000 USD',
    participantCount: 310,
    teamCount: 78,
    submissionCount: 72,
    tracks: [
      { id: 'trk_dt_01', name: 'IDE Extensions', description: 'VS Code and JetBrains extension tools.' }
    ],
    rubric: [
      { id: 'rub_dt_01', name: 'Developer UX', maxScore: 10, weight: 1.0, description: 'Seamless IDE integration.' }
    ]
  }
];

export const MOCK_HACKATHON = MOCK_HACKATHONS[0];
