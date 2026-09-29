import type { JudgeAssignment, Review } from './types';

export const MOCK_JUDGE_ASSIGNMENTS: JudgeAssignment[] = [
  {
    id: 'asg_01',
    judgeId: 'jdg_01',
    judgeName: 'Ada Okonkwo',
    submissionId: 'prj_01',
    submissionTitle: 'Quiet Hours',
    trackName: 'Developer Tools & Automation',
    status: 'COMPLETED'
  },
  {
    id: 'asg_02',
    judgeId: 'jdg_01',
    judgeName: 'Ada Okonkwo',
    submissionId: 'prj_02',
    submissionTitle: 'Glass Signal',
    trackName: 'Artificial Intelligence & Agents',
    status: 'PENDING'
  },
  {
    id: 'asg_03',
    judgeId: 'jdg_01',
    judgeName: 'Ada Okonkwo',
    submissionId: 'prj_03',
    submissionTitle: 'Deep Compass',
    trackName: 'Web3 & Decentralized Infrastructure',
    status: 'PENDING'
  }
];

export const MOCK_REVIEWS: Review[] = [
  {
    id: 'rev_01',
    submissionId: 'prj_01',
    judgeId: 'jdg_01',
    judgeName: 'Ada Okonkwo',
    status: 'SUBMITTED',
    scores: [
      { criterionId: 'rub_01', criterionName: 'Functionality & Architecture', score: 9.5 },
      { criterionId: 'rub_02', criterionName: 'User Experience & Interface', score: 9.0 },
      { criterionId: 'rub_03', criterionName: 'Technical Originality', score: 8.5 },
      { criterionId: 'rub_04', criterionName: 'Presentation & Pitch', score: 9.0 }
    ],
    comment: 'Outstanding architecture and clear utility for devops workloads. Highly scalable.',
    updatedAt: '2026-09-28T20:15:00Z'
  }
];
