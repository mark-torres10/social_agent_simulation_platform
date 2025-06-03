# Agent Simulation Platform

## Project Description
The Agent Simulation Platform is a research and experimentation tool for simulating social media agents and their interactions. It enables users to configure, run, and analyze multi-agent simulations, modeling how agents interact, consume feeds, update beliefs, and engage with content over multiple rounds. The platform is designed for extensibility, supporting advanced agent traits, memory management, and future integration with LLMs or custom engagement logic.

## What the App Does
- **Configurable Agent-Based Simulation:** Users can specify the number of agents and simulation rounds, with future support for custom personas and traits.
- **Interactive UI:** A Streamlit-based UI allows users to configure simulation parameters, initialize the simulation, run single or multiple rounds, and view results.
- **Backend Simulation Engine:** The backend manages agent initialization, feed generation, agent sessions (including scrolling, observation, engagement, and belief updating), and memory management.
- **Results Visualization:** Simulation results are displayed per day and per agent, showing agent profiles, feeds, thoughts, and actions in an intuitive, tabbed interface.
- **Extensible Architecture:** The codebase is modular, supporting future extensions for richer agent logic, export, and analysis.

## Environment Setup

### Python Package Setup
1. Create a virtual environment (e.g., `agent-simulation-platform`).
2. Install `pip-tools`.
3. Install the packages in `requirements.txt` and `dev_requirements.txt`:
   ```bash
   pip install -r requirements.txt
   pip install -r dev_requirements.txt
   ```

### Project Directory
- Set up `direnv` and run `direnv allow` in the project root to ensure the correct environment variables and local root directory are used.

## Usage
1. Launch the Streamlit UI:
   ```bash
   streamlit run ui/app.py
   ```
2. In the UI, configure the number of agents and simulation rounds.
3. Click **Initialize Simulation** to set up the simulation with your parameters.
4. Use **Simulate Round** to run a single round, or **Simulate Full Simulation** to run all rounds at once.
5. Explore results per day and per agent, including agent profiles, feeds, thoughts, and actions.

## Key Features
- UI/backend connection: Real-time configuration and results.
- Per-agent and per-day simulation with interactive exploration.
- Extensible agent traits and memory management.
- Export-ready architecture for future data analysis.

## Contributing & Planning
- See the `planning/` and `progress_updates/` directories for detailed design, planning, and progress tracking.
- Contributions are welcome! Please review the architecture and planning docs before submitting major changes.
