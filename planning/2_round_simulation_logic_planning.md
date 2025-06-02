# Round Simulation Logic Plan

## Problem Statement
- The simulation platform needs to support multi-round, multi-agent interactions to model realistic social media or agent-based environments.
- There is a need for a structured way to simulate each agent's actions, observations, and engagements within a round, and to update their beliefs accordingly.
- The system must be extensible for future features (e.g., more complex engagement, memory, or feed logic, LLM-based reasoning, and activity recording).

## Solution Overview
- Introduce `AgentSession` to encapsulate a single round of interaction for an agent, including feed scrolling, engagement, belief updating, and activity recording.
- Add `UserFeedManager`, `UserFeedScrollManager`, and `UserEngagementManager` to modularize feed loading, observation, and engagement logic. These now include stubs for LLM-based logic and are designed for future extension.
- Update `SimulationManager` to simulate rounds by running an `AgentSession` for each agent per round.
- The `Agent` class is now defined in `agent/agent.py` and includes an `update_beliefs` method for extensible belief management.
- `FeedPost`, `FeedObservation`, and `UserEngagement` now use improved metadata and support extensible, dictionary-based actions and engagement.
- Stubs for memory manager integration and activity recording are present for future work.
- All new logic is implemented in `simulation/agent_session.py` and integrated into `simulation/simulation_manager.py`.
- Design is modular and ready for future extension (e.g., LLM-based observation, richer engagement types, memory integration).

## UI/UX Plan
- Not applicable for this backend-only feature.

## Implementation Checklist
- [x] Implement `AgentSession` to encapsulate a single agent's round
- [x] Implement `UserFeedManager`, `UserFeedScrollManager`, and `UserEngagementManager` with extensible, LLM-ready stubs
- [x] Integrate round simulation logic into `SimulationManager`
- [x] Refactor `Agent` class to `agent/agent.py` and add `update_beliefs`
- [x] Improve metadata handling in `FeedPost`, `FeedObservation`, and `UserEngagement`
- [ ] Add unit tests for round simulation, agent session logic, and belief updating
- [ ] Integrate memory manager and implement activity recording
- [ ] Document public APIs and usage examples

## References
- planning/1_agent_initialization_and_management_planning.md
- simulation/agent_session.py
- simulation/simulation_manager.py
- agent/agent.py
- agent/initialize_agents.py
- agent/agent_manager.py

## Additional Notes
**All future bugs and improvements for this feature will be tracked in this file.** 