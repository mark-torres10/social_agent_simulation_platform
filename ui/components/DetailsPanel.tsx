'use client';

import { Run, Agent, Turn, Post, RunConfig } from '@/types';
import RunSummary from './RunSummary';
import AgentDetail from './AgentDetail';
import { getPostByUri } from '@/lib/dummy-data';

interface DetailsPanelProps {
  run: Run | null;
  turn: Turn | null;
  turnNumber: number | 'summary' | null;
  config: RunConfig | null;
  agents: Agent[];
}

export default function DetailsPanel({
  run,
  turn,
  turnNumber,
  config,
  agents,
}: DetailsPanelProps) {
  if (!run) {
    return (
      <div className="flex-1 flex items-center justify-center text-beige-600">
        Select a run to view details
      </div>
    );
  }

  if (turnNumber === 'summary' || turnNumber === null) {
    return <RunSummary run={run} agents={agents} />;
  }

  if (!turn) {
    return (
      <div className="flex-1 flex items-center justify-center text-beige-600">
        No turn data available
      </div>
    );
  }

  const allPosts = Object.values(turn.agentFeeds)
    .flatMap((feed) => feed.postUris.map((uri) => getPostByUri(uri)))
    .filter((p): p is Post => p !== undefined);

  return (
    <div className="flex-1 flex flex-col overflow-hidden">
      {/* Run Parameters */}
      {config && (
        <div className="p-4 border-b border-beige-300 bg-beige-50">
          <h3 className="text-sm font-medium text-beige-900 mb-2">Run Parameters</h3>
          <div className="text-sm text-beige-700 space-y-1">
            <div>Agents: {config.numAgents}</div>
            <div>Turns: {config.numTurns}</div>
          </div>
        </div>
      )}

      {/* Agents Container */}
      <div className="flex-1 overflow-y-auto p-6">
        <h3 className="text-lg font-medium text-beige-900 mb-4">Agents</h3>
        <div className="space-y-4">
          {agents.map((agent) => {
            const feed = turn.agentFeeds[agent.handle];
            const feedPosts = feed
              ? feed.postUris.map((uri) => getPostByUri(uri)).filter((p): p is Post => p !== undefined)
              : [];
            const agentActions = turn.agentActions[agent.handle] || [];

            return (
              <div key={agent.handle} className="border border-beige-300 rounded-lg p-3">
                <div className="font-medium text-beige-900 mb-2">
                  Agent {agent.name}
                </div>
                <AgentDetail
                  agent={agent}
                  feed={feedPosts}
                  actions={agentActions}
                  allPosts={allPosts}
                />
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

