'use client';

import { useState } from 'react';
import RunHistorySidebar from '@/components/RunHistorySidebar';
import ConfigForm from '@/components/ConfigForm';
import TurnHistorySidebar from '@/components/TurnHistorySidebar';
import DetailsPanel from '@/components/DetailsPanel';
import {
  DUMMY_RUNS,
  DUMMY_AGENTS,
  DUMMY_TURNS,
  DEFAULT_CONFIG,
} from '@/lib/dummy-data';
import { Run, RunConfig, Turn } from '@/types';

export default function Home() {
  const [runs, setRuns] = useState<Run[]>(DUMMY_RUNS);
  const [selectedRunId, setSelectedRunId] = useState<string | null>(null);
  const [selectedTurn, setSelectedTurn] = useState<number | 'summary' | null>(null);
  const [runConfig, setRunConfig] = useState<RunConfig | null>(null);
  const [newRunTurns, setNewRunTurns] = useState<Record<string, Record<string, Turn>>>({});

  const selectedRun = runs.find((r) => r.runId === selectedRunId) || null;
  const currentTurn: Turn | null =
    selectedRunId && typeof selectedTurn === 'number'
      ? (newRunTurns[selectedRunId]?.[selectedTurn.toString()] || 
         DUMMY_TURNS[selectedRunId]?.[selectedTurn.toString()] || null)
      : null;

  // Get agents for the selected run
  // For dummy data, use first N agents based on run.totalAgents
  // In a real implementation, this would fetch agents from the run data
  const getRunAgents = (run: Run | null): Agent[] => {
    if (!run) return DUMMY_AGENTS;
    // Use first N agents based on totalAgents count
    return DUMMY_AGENTS.slice(0, Math.min(run.totalAgents, DUMMY_AGENTS.length));
  };

  const runAgents = getRunAgents(selectedRun);

  const handleConfigSubmit = (config: RunConfig) => {
    // Create a new run
    const now = new Date();
    const newRunId = `run_${now.toISOString()}`;
    const newRun: Run = {
      runId: newRunId,
      createdAt: now.toISOString(),
      totalTurns: config.numTurns,
      totalAgents: config.numAgents,
      status: 'running',
    };

    // Add the new run to the list
    setRuns((prev) => [newRun, ...prev]);
    setRunConfig(config);
    setSelectedRunId(newRunId);
    setSelectedTurn('summary');
  };

  const handleSelectRun = (runId: string) => {
    setSelectedRunId(runId);
    setSelectedTurn('summary');
  };

  const handleSelectTurn = (turn: number | 'summary') => {
    setSelectedTurn(turn);
  };

  const handleStartNewRun = () => {
    setSelectedRunId(null);
    setSelectedTurn(null);
  };

  // Determine if we're in start screen or active run view
  const isStartScreen = selectedRunId === null;

  return (
    <div className="flex h-screen w-full bg-background overflow-hidden">
      {/* Left 1/4: Run History Sidebar */}
      <RunHistorySidebar
        runs={runs}
        selectedRunId={selectedRunId}
        onSelectRun={handleSelectRun}
        onStartNewRun={handleStartNewRun}
      />

      {isStartScreen ? (
        /* Right 3/4: Config Form (Start Screen) */
        <ConfigForm onSubmit={handleConfigSubmit} defaultConfig={DEFAULT_CONFIG} />
      ) : (
        <>
          {/* Second 1/4: Turn History Sidebar (when run is active) */}
          <TurnHistorySidebar
            totalTurns={selectedRun?.totalTurns || 0}
            selectedTurn={selectedTurn}
            onSelectTurn={handleSelectTurn}
          />

          {/* Right 2/4: Details Panel */}
          <DetailsPanel
            run={selectedRun}
            turn={currentTurn}
            turnNumber={selectedTurn}
            config={runConfig}
            agents={runAgents}
          />
        </>
      )}
    </div>
  );
}
