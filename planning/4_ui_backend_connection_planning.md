# UI/Backend Connection Plan

## Progress Update (2024-06-03)

### Latest Progress
- **UI/Backend Connection Complete:** The Streamlit UI is now fully connected to the backend. User-provided configuration (number of agents, number of turns) is passed to the backend and used to initialize the simulation. The simulation is only initialized when the user clicks the "Initialize Simulation" button.
- **Main Simulation Entry Point:** Added a main simulation entry point (`main.py`) for CLI and refactored the simulation manager to use explicit list type hints for agents and results.
- **Data Model Refactor:** Introduced and integrated new `Feed`, `FeedPost`, `FeedObservation`, and `UserEngagement` models. The agent session and simulation logic now use these structured models throughout.
- **UI Results Display:** The UI now displays real simulation results, with per-day (tabbed) and per-user (selectable) views. Each round's results are shown, including agent profiles, feeds, observations, and engagements.
- **MemoryManager Refactor:** The memory manager now robustly handles database creation, batch operations, and is integrated with the simulation lifecycle. Data is persisted and can be extended for future export/reload features.
- **Incremental Simulation:** Users can run single rounds or full simulations interactively from the UI, and results are accumulated and displayed.

### What's Completed (updated)
- [x] UI/backend connection: UI passes config to backend and displays real results.
- [x] Main simulation entry point and refactored agent/session logic.
- [x] Feed and UserEngagement models integrated throughout.
- [x] MemoryManager refactor and integration.
- [x] UI displays real simulation results, per day and per user.

### What's In Progress / Outstanding (updated)
- [ ] Advanced config: Support for agent personas, traits, and other settings in the UI/backend.
- [ ] Error/loading handling: Robust error and loading state handling in the UI.
- [ ] Export: Implement export of simulation results from backend to UI.
- [ ] End-to-end and automated tests for the full flow.
- [ ] UI/UX polish and accessibility improvements.

## Problem Statement
- The current UI (Streamlit) is fully stubbed and does not interact with the backend simulation logic.
- Users cannot run real simulations or see real results; all data is placeholder.
- There is no mechanism for passing configuration from the UI to the backend, triggering simulation runs, or displaying actual simulation results.
- The backend expects configuration via `SimulationConfig` and `AgentConfig`, but these are not populated from the UI.

## Solution Overview
- Implement a connection layer between the UI and backend logic.
- Allow the UI to collect agent and simulation configuration, pass it to the backend, and trigger simulation runs.
- Display real simulation results in the UI, replacing stubs.
- Use Streamlit session state or callbacks to manage state and trigger backend calls.
- Update or extend `SimulationConfig` and `AgentConfig` to accept parameters from the UI.
- Reference files: `ui/app.py`, `ui/components/config/agent_config.py`, `ui/components/config/simulation_config.py`, `simulation/simulation_manager.py`, `config/models.py`.

---

## Detailed UI/Backend Connection Plan

### 1. Data Flow: UI to Backend

#### a. Collecting Configuration in the UI
- Refactor UI config components to return configuration values (e.g., as dicts or dataclasses) to `ui/app.py`.
- Example: `num_agents`, `persona_choice`, `num_turns`, etc.
- Consider returning a tuple or config object.

#### b. Passing Configuration to Backend
- Define all required fields in `SimulationConfig` and `AgentConfig` (e.g., number of agents, agent traits, number of rounds, etc.).
- In `ui/app.py`, instantiate these config objects using values returned from the UI components.
- When the user clicks "Start Simulation", pass these config objects to `SimulationManager`.

#### c. Triggering Simulation Runs
- On button click, call a function that:
    1. Instantiates `SimulationManager` with the collected config.
    2. Calls `init_agents()`, `init_simulation()`, and `simulate_rounds(num_rounds)`.
    3. Collects results for display in the UI.
- Use Streamlit's session state to store config and results for persistence across reruns.

---

### 2. Data Flow: Backend to UI

#### a. Collecting and Returning Results
- Refactor `SimulationManager` and/or `AgentSession` to collect and return simulation results (e.g., per-agent feeds, actions, metrics) as structured data (lists/dicts/models).
- Add a method like `get_simulation_results()` to `SimulationManager` that returns all relevant data for UI display.
- Ensure that after each simulation run, results are available for the UI to render.

#### b. Displaying Results in the UI
- Replace stubbed data in the UI with real results from the backend.
- Use Streamlit components (tabs, expanders, tables, charts) to display feeds, agent thoughts, actions, metrics, etc.
- Handle loading states and errors gracefully.

---

### 3. Data Persistence and I/O

#### a. Using `memory_manager.py`
- Implement missing methods in `MemoryManager`:
    - `add_item_to_db`, `load_memory`, `load_memories`, `save_memory`, `save_memories`.
    - Ensure these methods can persist and retrieve agent state, feed history, and simulation results.
- Implement `AgentMemoryManager` to manage all memories for a given agent.
- Ensure `GlobalMemoryManager` can initialize, save, and load all relevant simulation data.
- Integrate memory management into the simulation run so that results and state are persisted and can be reloaded for display or further analysis.

#### b. Exposing Data for UI
- Add methods to `SimulationManager` or a new API layer to fetch persisted results for display or export.
- Consider adding a method like `load_previous_simulation_results()` for the UI to call.

---

### 4. Missing or Underspecified Functions/Methods

#### a. In `simulation_manager.py`:
- `export_simulation_results`: Needs to be implemented to return/export results in a structured format.
- `get_simulation_results` (recommended): Add a method to return all results for UI consumption.

#### b. In `agent_session.py`:
- `UserFeedManager.load_latest_feed`: Needs implementation to return a feed for the agent.
- `AgentSession.record_activity`: Needs implementation to persist agent actions and state.

#### c. In `memory_manager.py`:
- All CRUD methods: `add_item_to_db`, `load_memory`, `load_memories`, `save_memory`, `save_memories` are currently stubs and must be implemented.
- `AgentMemoryManager`: Needs full implementation for per-agent memory management.

#### d. In `config/models.py`:
- `SimulationConfig/AgentConfig`: Need to be fully defined with all fields required for simulation and agent initialization.

#### e. In the UI:
- `agent_config_component/simulation_config_component`: Should return values to the main app.
- UI logic: Should handle loading, error, and result display states.

---

### 5. Example End-to-End Flow

1. User configures simulation in the UI.
2. UI collects config and instantiates `SimulationConfig`/`AgentConfig`.
3. User clicks "Start Simulation".
4. UI calls backend:
    - Instantiates `SimulationManager` with config.
    - Runs simulation.
    - Collects results.
    - Persists results via `memory_manager.py`.
5. UI displays results using real data.
6. User can export or reload results as needed.

---

### 6. Recommendations for Robustness

- Use Pydantic models for all data passed between UI and backend for validation and clarity.
- Ensure all backend methods return structured data, not just print/log output.
- Use Streamlit session state to manage UI state and results.
- Implement error handling and user feedback for all backend calls.

---

### 7. Implementation Checklist (Expanded)

- [x] Refactor UI config components to return values.
- [x] Define all fields in `SimulationConfig` and `AgentConfig`.
- [x] Implement all missing methods in `memory_manager.py`.
- [x] Refactor `SimulationManager` to return results for UI.
- [ ] Implement result display in the UI.
- [ ] Add error/loading handling in the UI.
- [ ] Manual and automated tests for end-to-end flow.

## References
- planning/3_ui_first_pass_planning.md
- planning/2_round_simulation_logic_planning.md
- architecture/1_v1_design.md
- ui/app.py
- simulation/simulation_manager.py
- config/models.py

## Additional Notes
**All future bugs and improvements for UI/backend connection will be tracked in this file.** 