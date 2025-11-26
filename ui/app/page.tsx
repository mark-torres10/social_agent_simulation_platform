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
import { Run, RunConfig, Turn, Agent } from '@/types';

export default function Home() {
  const [runs, setRuns] = useState<Run[]>(DUMMY_RUNS.map((run) => ({
    ...run,
    status: (() => {
      const turns = DUMMY_TURNS[run.runId] || {};
      const completed = Object.keys(turns).length;
      return completed >= run.totalTurns ? 'completed' : 'running';
    })(),
  })));
  const [selectedRunId, setSelectedRunId] = useState<string | null>(null);
  const [selectedTurn, setSelectedTurn] = useState<number | 'summary' | null>(null);
  const [runConfigs, setRunConfigs] = useState<Record<string, RunConfig>>({});
  const [newRunTurns, setNewRunTurns] = useState<Record<string, Record<string, Turn>>>({});

  const selectedRun = runs.find((r) => r.runId === selectedRunId) || null;
  const currentTurn: Turn | null =
    selectedRunId && typeof selectedTurn === 'number'
      ? (newRunTurns[selectedRunId]?.[selectedTurn.toString()] || 
         DUMMY_TURNS[selectedRunId]?.[selectedTurn.toString()] || null)
      : null;

  // Get available turns for a run (turns that have data)
  const getAvailableTurns = (runId: string | null): number[] => {
    if (!runId) return [];
    const turns = newRunTurns[runId] || DUMMY_TURNS[runId] || {};
    return Object.keys(turns)
      .map(Number)
      .sort((a, b) => a - b);
  };

  // Get completed turns count for a run
  const getCompletedTurnsCount = (runId: string | null): number => {
    return getAvailableTurns(runId).length;
  };

  // Get agents for the selected run
  // For dummy data, use first N agents based on run.totalAgents
  // In a real implementation, this would fetch agents from the run data
  const getRunAgents = (run: Run | null): Agent[] => {
    if (!run) return DUMMY_AGENTS;
    // Use first N agents based on totalAgents count
    return DUMMY_AGENTS.slice(0, Math.min(run.totalAgents, DUMMY_AGENTS.length));
  };

  const runAgents = getRunAgents(selectedRun);
  const availableTurns = getAvailableTurns(selectedRunId);
  const completedTurnsCount = getCompletedTurnsCount(selectedRunId);

  // Get the config for the selected run
  // For dummy runs, derive from Run data; for new runs, get from stored configs
  const getRunConfig = (run: Run | null): RunConfig | null => {
    if (!run) return null;
    // Check if we have a stored config for this run
    if (runConfigs[run.runId]) {
      return runConfigs[run.runId];
    }
    // For dummy runs, derive config from Run data
    return {
      numAgents: run.totalAgents,
      numTurns: run.totalTurns,
    };
  };

  const currentRunConfig = getRunConfig(selectedRun);

  // Update run status based on completed vs total turns
  const getRunStatus = (run: Run | null): 'running' | 'completed' | 'failed' => {
    if (!run) return 'running';
    const completed = getCompletedTurnsCount(run.runId);
    return completed >= run.totalTurns ? 'completed' : 'running';
  };

  // Update runs with computed status (memoized computation)
  const runsWithStatus = runs.map((run) => ({
    ...run,
    status: getRunStatus(run),
  }));

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
    // Store the config keyed by runId
    setRunConfigs((prev) => ({ ...prev, [newRunId]: config }));
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
        runs={runsWithStatus}
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
            availableTurns={availableTurns}
            selectedTurn={selectedTurn}
            onSelectTurn={handleSelectTurn}
          />

          {/* Right 2/4: Details Panel */}
          <DetailsPanel
            run={selectedRun ? { ...selectedRun, status: getRunStatus(selectedRun) } : null}
            turn={currentTurn}
            turnNumber={selectedTurn}
            config={currentRunConfig}
            agents={runAgents}
            completedTurns={completedTurnsCount}
          />
        </>
      )}
    </div>
  );
}
