import { Run, Agent, Post, Turn, RunConfig, Feed, AgentAction } from '@/types';

export const DUMMY_RUNS: Run[] = [
  {
    runId: 'run_2025-01-15T10:30:00',
    createdAt: '2025-01-15T10:30:00',
    totalTurns: 10,
    totalAgents: 3,
    status: 'completed', // Will be updated based on actual turns
  },
  {
    runId: 'run_2025-01-15T14:45:00',
    createdAt: '2025-01-15T14:45:00',
    totalTurns: 10,
    totalAgents: 4,
    status: 'running', // Will be updated based on actual turns
  },
  {
    runId: 'run_2025-01-16T09:15:00',
    createdAt: '2025-01-16T09:15:00',
    totalTurns: 5,
    totalAgents: 3,
    status: 'running', // Will be updated based on actual turns
  },
  {
    runId: 'run_2025-01-17T08:20:00',
    createdAt: '2025-01-17T08:20:00',
    totalTurns: 15,
    totalAgents: 4,
    status: 'running', // Will be updated based on actual turns
  },
  {
    runId: 'run_2025-01-18T11:00:00',
    createdAt: '2025-01-18T11:00:00',
    totalTurns: 20,
    totalAgents: 4,
    status: 'running', // Will be updated based on actual turns
  },
];

export const DUMMY_AGENTS: Agent[] = [
  {
    handle: '@alice.bsky.social',
    name: 'Alice Chen',
    bio: 'AI researcher and educator. Building the future of human-AI collaboration.',
    generatedBio: 'Alice is a passionate AI researcher who focuses on making artificial intelligence more accessible and understandable. She regularly shares insights about machine learning, human-computer interaction, and the ethical implications of AI technology.',
    followers: 12450,
    following: 892,
    postsCount: 3421,
  },
  {
    handle: '@bob.tech',
    name: 'Bob Martinez',
    bio: 'Software engineer | Open source contributor | Coffee enthusiast ☕',
    generatedBio: 'Bob is an experienced software engineer with a strong focus on open-source contributions. He loves sharing technical knowledge, code reviews, and occasionally posts about his coffee adventures.',
    followers: 8765,
    following: 1203,
    postsCount: 2105,
  },
  {
    handle: '@charlie.dev',
    name: 'Charlie Kim',
    bio: 'Building products that matter. Former startup founder.',
    generatedBio: 'Charlie is a product-focused engineer with a background in startup entrepreneurship. He shares lessons learned, product development insights, and thoughts on building sustainable businesses.',
    followers: 15432,
    following: 567,
    postsCount: 4521,
  },
  {
    handle: '@diana.design',
    name: 'Diana Park',
    bio: 'UX Designer | Accessibility advocate | Design systems enthusiast',
    generatedBio: 'Diana is a UX designer passionate about creating inclusive and accessible digital experiences. She frequently shares design system patterns, accessibility best practices, and thoughts on how design impacts user behavior.',
    followers: 9876,
    following: 1456,
    postsCount: 1876,
  },
  {
    handle: '@edward.data',
    name: 'Edward Wu',
    bio: 'Data scientist | ML engineer | Stats nerd 📊',
    generatedBio: 'Edward is a data scientist who loves diving deep into datasets and building machine learning models. He shares analysis insights, statistical findings, and practical ML techniques with the community.',
    followers: 11234,
    following: 789,
    postsCount: 3210,
  },
  {
    handle: '@fiona.frontend',
    name: 'Fiona Lee',
    bio: 'Frontend engineer | React enthusiast | CSS wizard',
    generatedBio: 'Fiona is a frontend engineer specializing in React and modern CSS. She enjoys building performant web applications and sharing tips on component architecture, performance optimization, and creative CSS techniques.',
    followers: 6543,
    following: 923,
    postsCount: 1567,
  },
  {
    handle: '@george.backend',
    name: 'George Thompson',
    bio: 'Backend engineer | Distributed systems | Database optimization',
    generatedBio: 'George is a backend engineer with expertise in distributed systems and database design. He shares insights on system architecture, scalability challenges, and database performance tuning strategies.',
    followers: 14567,
    following: 612,
    postsCount: 2890,
  },
  {
    handle: '@hannah.ai',
    name: 'Hannah Rodriguez',
    bio: 'AI product manager | ML adoption | Ethical AI',
    generatedBio: 'Hannah is a product manager focused on bringing AI products to market. She writes about ML adoption strategies, ethical considerations in AI development, and bridging the gap between technical teams and business stakeholders.',
    followers: 8765,
    following: 1345,
    postsCount: 2103,
  },
];

export const DUMMY_POSTS: Post[] = [
  {
    uri: 'at://did:plc:example1/post1',
    authorDisplayName: 'Alice Chen',
    authorHandle: '@alice.bsky.social',
    text: 'Just finished reading an amazing paper on transformer architectures. The attention mechanism continues to surprise me with its elegance!',
    bookmarkCount: 23,
    likeCount: 145,
    quoteCount: 8,
    replyCount: 12,
    repostCount: 34,
    createdAt: '2025-01-15T10:00:00',
  },
  {
    uri: 'at://did:plc:example2/post2',
    authorDisplayName: 'Bob Martinez',
    authorHandle: '@bob.tech',
    text: 'Found a beautiful bug today that only shows up on Tuesdays during leap years. Classic. 🐛',
    bookmarkCount: 5,
    likeCount: 67,
    quoteCount: 2,
    replyCount: 8,
    repostCount: 12,
    createdAt: '2025-01-15T11:30:00',
  },
  {
    uri: 'at://did:plc:example3/post3',
    authorDisplayName: 'Charlie Kim',
    authorHandle: '@charlie.dev',
    text: 'The best product decisions are often the ones that seem obvious in retrospect but were controversial at the time.',
    bookmarkCount: 89,
    likeCount: 234,
    quoteCount: 15,
    replyCount: 45,
    repostCount: 78,
    createdAt: '2025-01-15T13:00:00',
  },
  {
    uri: 'at://did:plc:example4/post4',
    authorDisplayName: 'Diana Park',
    authorHandle: '@diana.design',
    text: 'Accessibility isn\'t optional. Every design decision impacts real people with real needs. Let\'s build for everyone. ♿',
    bookmarkCount: 156,
    likeCount: 423,
    quoteCount: 28,
    replyCount: 67,
    repostCount: 112,
    createdAt: '2025-01-15T14:15:00',
  },
  {
    uri: 'at://did:plc:example5/post5',
    authorDisplayName: 'Edward Wu',
    authorHandle: '@edward.data',
    text: 'Just visualized a dataset with 10M rows and the patterns that emerged were fascinating. Sometimes you need to zoom out to see the forest for the trees.',
    bookmarkCount: 34,
    likeCount: 198,
    quoteCount: 12,
    replyCount: 23,
    repostCount: 45,
    createdAt: '2025-01-15T15:30:00',
  },
  {
    uri: 'at://did:plc:example6/post6',
    authorDisplayName: 'Fiona Lee',
    authorHandle: '@fiona.frontend',
    text: 'CSS Grid + Flexbox = unstoppable. Just built a responsive layout that would have taken me hours before. Modern CSS is magical.',
    bookmarkCount: 78,
    likeCount: 312,
    quoteCount: 19,
    replyCount: 34,
    repostCount: 89,
    createdAt: '2025-01-15T16:00:00',
  },
  {
    uri: 'at://did:plc:example7/post7',
    authorDisplayName: 'George Thompson',
    authorHandle: '@george.backend',
    text: 'Database indexing is like a library catalog system. Without it, you\'re searching through every book. With it, you go straight to the shelf.',
    bookmarkCount: 112,
    likeCount: 445,
    quoteCount: 31,
    replyCount: 56,
    repostCount: 123,
    createdAt: '2025-01-15T17:20:00',
  },
  {
    uri: 'at://did:plc:example8/post8',
    authorDisplayName: 'Hannah Rodriguez',
    authorHandle: '@hannah.ai',
    text: 'The hardest part of building AI products isn\'t the technology—it\'s understanding user needs and ensuring the AI actually solves real problems.',
    bookmarkCount: 67,
    likeCount: 289,
    quoteCount: 22,
    replyCount: 41,
    repostCount: 98,
    createdAt: '2025-01-15T18:45:00',
  },
  {
    uri: 'at://did:plc:example9/post9',
    authorDisplayName: 'Alice Chen',
    authorHandle: '@alice.bsky.social',
    text: 'Reading through code reviews and learning so much. The best teams learn from each other. Always ask "why?" not just "what?"',
    bookmarkCount: 45,
    likeCount: 178,
    quoteCount: 9,
    replyCount: 19,
    repostCount: 42,
    createdAt: '2025-01-16T09:00:00',
  },
  {
    uri: 'at://did:plc:example10/post10',
    authorDisplayName: 'Bob Martinez',
    authorHandle: '@bob.tech',
    text: 'Refactored a legacy component today. It\'s like archaeology—carefully removing layers to discover the original intent. Satisfying when it all clicks.',
    bookmarkCount: 28,
    likeCount: 134,
    quoteCount: 6,
    replyCount: 15,
    repostCount: 29,
    createdAt: '2025-01-16T10:30:00',
  },
];

function createTurnForRun(
  runId: string,
  turnNumber: number,
  agents: Agent[],
  allPosts: Post[],
): Turn {
  // Rotate agent selection based on turnNumber to give different agents turns
  const startOffset = turnNumber % agents.length;
  const numAgents = Math.min(agents.length, 5);
  const selectedAgents: Agent[] = [];
  for (let i = 0; i < numAgents; i++) {
    const idx = (startOffset + i) % agents.length;
    selectedAgents.push(agents[idx]);
  }
  const agentFeeds: Record<string, Feed> = {};
  const agentActions: Record<string, AgentAction[]> = {};

  selectedAgents.forEach((agent, idx) => {
    // Each agent gets a different subset of posts
    const postStartIdx = (turnNumber * selectedAgents.length + idx) % allPosts.length;
    const postUris = [
      allPosts[postStartIdx % allPosts.length]?.uri,
      allPosts[(postStartIdx + 1) % allPosts.length]?.uri,
      allPosts[(postStartIdx + 2) % allPosts.length]?.uri,
    ].filter(Boolean) as string[];

    agentFeeds[agent.handle] = {
      feedId: `feed_${runId}_turn${turnNumber}_${agent.handle}`,
      runId,
      turnNumber,
      agentHandle: agent.handle,
      postUris,
      createdAt: new Date(Date.now() + turnNumber * 60000).toISOString(),
    };

    // Some agents take actions, some don't
    const actions: AgentAction[] = [];
    if (turnNumber % 2 === 0 && idx % 2 === 0 && postUris.length > 0) {
      actions.push({
        actionId: `action_${runId}_turn${turnNumber}_${agent.handle}_1`,
        agentHandle: agent.handle,
        postUri: postUris[0],
        type: 'like' as const,
        createdAt: new Date(Date.now() + turnNumber * 60000 + 5000).toISOString(),
      });
    }
    if (turnNumber % 3 === 0 && idx === 0 && selectedAgents.length > 1) {
      actions.push({
        actionId: `action_${runId}_turn${turnNumber}_${agent.handle}_2`,
        agentHandle: agent.handle,
        userId: selectedAgents[1].handle,
        type: 'follow' as const,
        createdAt: new Date(Date.now() + turnNumber * 60000 + 7000).toISOString(),
      });
    }
    agentActions[agent.handle] = actions;
  });

  return {
    turnNumber,
    agentFeeds,
    agentActions,
  };
}

export const DUMMY_TURNS: Record<string, Record<string, Turn>> = {
  // Complete run: all 10 turns completed
  'run_2025-01-15T10:30:00': {
    '0': createTurnForRun('run_2025-01-15T10:30:00', 0, DUMMY_AGENTS.slice(0, 3), DUMMY_POSTS),
    '1': createTurnForRun('run_2025-01-15T10:30:00', 1, DUMMY_AGENTS.slice(0, 3), DUMMY_POSTS),
    '2': createTurnForRun('run_2025-01-15T10:30:00', 2, DUMMY_AGENTS.slice(0, 3), DUMMY_POSTS),
    '3': createTurnForRun('run_2025-01-15T10:30:00', 3, DUMMY_AGENTS.slice(0, 3), DUMMY_POSTS),
    '4': createTurnForRun('run_2025-01-15T10:30:00', 4, DUMMY_AGENTS.slice(0, 3), DUMMY_POSTS),
    '5': createTurnForRun('run_2025-01-15T10:30:00', 5, DUMMY_AGENTS.slice(0, 3), DUMMY_POSTS),
    '6': createTurnForRun('run_2025-01-15T10:30:00', 6, DUMMY_AGENTS.slice(0, 3), DUMMY_POSTS),
    '7': createTurnForRun('run_2025-01-15T10:30:00', 7, DUMMY_AGENTS.slice(0, 3), DUMMY_POSTS),
    '8': createTurnForRun('run_2025-01-15T10:30:00', 8, DUMMY_AGENTS.slice(0, 3), DUMMY_POSTS),
    '9': createTurnForRun('run_2025-01-15T10:30:00', 9, DUMMY_AGENTS.slice(0, 3), DUMMY_POSTS),
  },
  // Incomplete run: only 3 of 10 turns completed
  'run_2025-01-15T14:45:00': {
    '0': createTurnForRun('run_2025-01-15T14:45:00', 0, DUMMY_AGENTS.slice(0, 4), DUMMY_POSTS),
    '1': createTurnForRun('run_2025-01-15T14:45:00', 1, DUMMY_AGENTS.slice(0, 4), DUMMY_POSTS),
    '2': createTurnForRun('run_2025-01-15T14:45:00', 2, DUMMY_AGENTS.slice(0, 4), DUMMY_POSTS),
  },
  // Complete run: all 5 turns completed
  'run_2025-01-16T09:15:00': {
    '0': createTurnForRun('run_2025-01-16T09:15:00', 0, DUMMY_AGENTS.slice(0, 3), DUMMY_POSTS),
    '1': createTurnForRun('run_2025-01-16T09:15:00', 1, DUMMY_AGENTS.slice(0, 3), DUMMY_POSTS),
    '2': createTurnForRun('run_2025-01-16T09:15:00', 2, DUMMY_AGENTS.slice(0, 3), DUMMY_POSTS),
    '3': createTurnForRun('run_2025-01-16T09:15:00', 3, DUMMY_AGENTS.slice(0, 3), DUMMY_POSTS),
    '4': createTurnForRun('run_2025-01-16T09:15:00', 4, DUMMY_AGENTS.slice(0, 3), DUMMY_POSTS),
  },
  // Incomplete run: only 8 of 15 turns completed
  'run_2025-01-17T08:20:00': {
    '0': createTurnForRun('run_2025-01-17T08:20:00', 0, DUMMY_AGENTS.slice(0, 4), DUMMY_POSTS),
    '1': createTurnForRun('run_2025-01-17T08:20:00', 1, DUMMY_AGENTS.slice(0, 4), DUMMY_POSTS),
    '2': createTurnForRun('run_2025-01-17T08:20:00', 2, DUMMY_AGENTS.slice(0, 4), DUMMY_POSTS),
    '3': createTurnForRun('run_2025-01-17T08:20:00', 3, DUMMY_AGENTS.slice(0, 4), DUMMY_POSTS),
    '4': createTurnForRun('run_2025-01-17T08:20:00', 4, DUMMY_AGENTS.slice(0, 4), DUMMY_POSTS),
    '5': createTurnForRun('run_2025-01-17T08:20:00', 5, DUMMY_AGENTS.slice(0, 4), DUMMY_POSTS),
    '6': createTurnForRun('run_2025-01-17T08:20:00', 6, DUMMY_AGENTS.slice(0, 4), DUMMY_POSTS),
    '7': createTurnForRun('run_2025-01-17T08:20:00', 7, DUMMY_AGENTS.slice(0, 4), DUMMY_POSTS),
  },
  // Incomplete run: only 5 of 20 turns completed
  'run_2025-01-18T11:00:00': {
    '0': createTurnForRun('run_2025-01-18T11:00:00', 0, DUMMY_AGENTS.slice(0, 4), DUMMY_POSTS),
    '1': createTurnForRun('run_2025-01-18T11:00:00', 1, DUMMY_AGENTS.slice(0, 4), DUMMY_POSTS),
    '2': createTurnForRun('run_2025-01-18T11:00:00', 2, DUMMY_AGENTS.slice(0, 4), DUMMY_POSTS),
    '3': createTurnForRun('run_2025-01-18T11:00:00', 3, DUMMY_AGENTS.slice(0, 4), DUMMY_POSTS),
    '4': createTurnForRun('run_2025-01-18T11:00:00', 4, DUMMY_AGENTS.slice(0, 4), DUMMY_POSTS),
  },
};

export const DEFAULT_CONFIG: RunConfig = {
  numAgents: 5,
  numTurns: 10,
};

export function getPostByUri(uri: string): Post | undefined {
  return DUMMY_POSTS.find((p) => p.uri === uri);
}

export function getAgentByHandle(handle: string): Agent | undefined {
  return DUMMY_AGENTS.find((a) => a.handle === handle);
}

