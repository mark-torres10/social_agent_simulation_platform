# UI First Pass (Stub) Plan

## Problem Statement
- There is currently no user interface for configuring, running, or visualizing the agent simulation platform.
- Users need a clear, interactive UI to configure agents, run simulations, and view results (feeds, agent actions, network, metrics).
- The UI must follow modern usability and design standards, and be ready for future extension and backend integration.

## Solution Overview
- Implement a first-pass UI in `/ui/app.py` and `/ui/components/` as proposed in `architecture/1_v1_design.md` and `PROPOSED_UI.md`.
- Use Streamlit for rapid prototyping and adherence to UI guidelines.
- Stub all data and logic with placeholders; no backend integration yet.
- Structure UI into logical sections: configuration, simulation control, per-user feed/actions, network summary, metrics, and export.
- Follow all rules in `rules/RULES.md` and design principles in `rules/UI_PRINCIPLES.md`.

## UI/UX Plan
- **Layout**: Use a clean, column-based layout with clear sectioning (Streamlit `st.columns`, `st.container`).
- **Agent Configuration**: Section for number of agents, personas, and other config (inputs, dropdowns, defaults).
- **Simulation Configuration**: Section for number of turns, start button.
- **Simulation View**:
  - For each day/round, show each user's feed in a 3-column layout:
    - Feed posts (UserFeedPostComponent)
    - Agent thoughts (placeholder text)
    - Actions (like, comment, etc. as buttons or icons)
  - Show user actions and opinion changes below feed.
- **Network Summary**:
  - Social network visualization (placeholder chart or image)
  - Aggregate statistics (metrics, KPIs, number of changed opinions, etc.)
- **Total Simulation Metrics**: Section for overall stats at end of simulation.
- **Export**: Button to export simulation data (stub only).
- **Design**: Adhere to clarity, hierarchy, spacing, and color guidelines from `UI_PRINCIPLES.md`.
- **Accessibility**: Use readable font sizes, contrast, and clear labels.
- **Progressive Disclosure**: Show essential info first, details on demand.

## Implementation Checklist
- [ ] Create `/ui/` directory and `app.py` entrypoint
- [ ] Create `/ui/components/` subdirectory and stub files:
    - `config/agent_config.py`, `config/simulation_config.py`
    - `user/user.py`, `user/user_feed.py`, `user/user_feed_posts.py`, `user/user_feed_observations.py`, `user/user_feed_interactions.py`
    - `network/social_network.py`
    - `analysis/analyze_network.py`
- [ ] Implement main UI layout in `app.py` with placeholder data
- [ ] Implement agent and simulation config sections (inputs, dropdowns)
- [ ] Implement per-user feed view with 3-column layout and stub components
- [ ] Implement user actions and opinion changes section
- [ ] Implement network summary section with placeholder visualization and metrics
- [ ] Implement total simulation metrics section
- [ ] Implement export button (stub)
- [ ] Ensure all UI follows `UI_PRINCIPLES.md` and `RULES.md`
- [ ] Add comments and docstrings for clarity
- [ ] Manual test for layout, clarity, and usability

## References
- architecture/1_v1_design.md
- PROPOSED_UI.md
- rules/UI_PRINCIPLES.md
- rules/RULES.md
- planning/FORMAT.md
- progress_updates/2_round_simulation_logic.md
- progress_updates/1_agent_initialization_and_management.md

## Additional Notes
**All future bugs and improvements for the UI will be tracked in this file.**

## Completion Notes (2024-06-01)
- The first pass of the UI is now implemented and fully stubbed.
- All planned sections are present: agent configuration, simulation configuration, simulation view (with days, users, and posts), network summary, metrics, and export.
- The Simulation View uses Streamlit tabs for days and users, and vertically stacked expanders for posts, to provide intuitive navigation and avoid nested expanders (per Streamlit API constraints).
- All content is placeholder/stubbed, ready for future backend integration.
- See progress_updates/3_ui_first_pass.md for detailed implementation notes and summary. 