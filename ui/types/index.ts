export interface Run {
  runId: string;
  createdAt: string;
  totalTurns: number;
  totalAgents: number;
  status: 'running' | 'completed' | 'failed';
}

export interface Agent {
  handle: string;
  name: string;
  bio: string;
  generatedBio: string;
  followers: number;
  following: number;
  postsCount: number;
}

export interface Post {
  uri: string;
  authorDisplayName: string;
  authorHandle: string;
  text: string;
  bookmarkCount: number;
  likeCount: number;
  quoteCount: number;
  replyCount: number;
  repostCount: number;
  createdAt: string;
}

export interface Feed {
  feedId: string;
  runId: string;
  turnNumber: number;
  agentHandle: string;
  postUris: string[];
  createdAt: string;
}

export interface AgentAction {
  actionId: string;
  agentHandle: string;
  postUri?: string;
  userId?: string;
  type: 'like' | 'comment' | 'follow';
  createdAt: string;
}

export interface Turn {
  turnNumber: number;
  agentFeeds: Record<string, Feed>;
  agentActions: Record<string, AgentAction[]>;
}

export interface RunConfig {
  numAgents: number;
  numTurns: number;
}

