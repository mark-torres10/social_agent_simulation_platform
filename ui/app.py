"""
Main entrypoint for the Agent Simulation Platform UI (first pass, stub only).
Follows the plan in planning/3_ui_first_pass_planning.md.
"""

import streamlit as st
from simulation.simulation_manager import SimulationManager

# Import stub components
from ui.components.network.social_network import social_network_component
from ui.components.analysis.analyze_network import analyze_network_component

st.set_page_config(page_title="AI Agent Simulation Platform", layout="wide")

st.title("AI Agent Simulation Platform")


# --- Agent and Simulation Configuration Section ---
def agent_config_component():
    st.header("Agent Configuration")
    st.caption("Configure the agents that will participate in the simulation.")
    st.subheader("Number of Agents")
    num_agents = st.number_input(
        "Select number of agents",
        min_value=1,
        max_value=100,
        value=5,
        key="num_agents_input",
    )
    st.subheader("Agent Personas")
    st.write("Not completed yet")
    persona_options = ["Default", "Custom"]
    persona_choice = st.selectbox(
        "Choose persona type", persona_options, key="persona_choice"
    )
    if persona_choice == "Custom":
        st.text_area("Enter custom persona descriptions (one per line)")
    else:
        st.write("Using default personas.")
    st.subheader("Other Settings")
    st.write("Not completed yet")
    return num_agents


def simulation_config_component():
    st.header("Simulation Configuration")
    st.caption("Configure the simulation parameters (e.g., number of turns).")
    st.subheader("Number of Turns")
    num_turns = st.number_input(
        "Select number of turns",
        min_value=1,
        max_value=100,
        value=10,
        key="num_turns_input",
    )
    st.subheader("Other Simulation Parameters")
    st.write("[Stub] Additional simulation configuration options will go here.")
    return num_turns


# --- Render configuration sections in order ---
num_agents = agent_config_component()
num_turns = simulation_config_component()

# --- Initialize Simulation Button ---
if st.button("Initialize Simulation"):
    st.session_state.sim_manager = SimulationManager()
    st.session_state.sim_manager.config.num_agents = num_agents
    st.session_state.sim_manager.init_agents()
    st.session_state.sim_manager.init_simulation()
    st.session_state.last_round_results = None
    st.session_state.all_round_results = []
    st.session_state.last_num_agents = num_agents
    st.session_state.last_num_turns = num_turns

sim_manager = st.session_state.get("sim_manager", None)

# --- Agents Section ---
st.header("Agents")
st.caption("View and inspect the initialized agents.")

if sim_manager is None:
    st.info("Please initialize the simulation using the button above.")
else:
    # Create a scrollable selectbox for user selection
    user_labels = [f"User {i+1}" for i in range(len(sim_manager.agents))]
    selected_idx = st.selectbox(
        "Select a user to view",
        options=list(range(len(user_labels))),
        format_func=lambda i: user_labels[i],
        key="user_selectbox",
    )

    # Optional: Add minimal CSS to ensure selectbox dropdown is scrollable (Streamlit default is already scrollable)
    st.markdown(
        """
        <style>
        div[data-baseweb=\"select\"] > div {
            max-height: 200px;
            overflow-y: auto;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    # Show the selected agent's profile in an expander
    agent = sim_manager.agents[selected_idx]
    with st.expander("Profile", expanded=False):
        st.markdown(agent.profile.get_profile_description())

    # --- Simulate Round Button ---
    if st.button("Simulate Round"):
        round_results = sim_manager.simulate_round()
        if "all_round_results" not in st.session_state:
            st.session_state.all_round_results = []
        st.session_state.all_round_results.append(round_results)
        st.session_state.last_round_results = round_results

    # --- Simulate Full Simulation Button ---
    if st.button("Simulate Full Simulation"):
        st.session_state.all_round_results = []
        for _ in range(num_turns):
            round_results = sim_manager.simulate_round()
            st.session_state.all_round_results.append(round_results)
        st.session_state.last_round_results = (
            st.session_state.all_round_results[-1]
            if st.session_state.all_round_results
            else None
        )

    # --- Simulation View Section ---
    st.header("Simulation View")

    # Only show if there are any rounds simulated
    if "all_round_results" in st.session_state and st.session_state.all_round_results:
        num_days = len(st.session_state.all_round_results)
        day_tabs = st.tabs([f"Day {i+1}" for i in range(num_days)])
        for day_idx, (day_tab, round_results) in enumerate(
            zip(day_tabs, st.session_state.all_round_results)
        ):
            with day_tab:
                # Scrollable selectbox for users in this round
                user_labels = [f"User {i+1}" for i in range(len(round_results))]
                selected_idx = st.selectbox(
                    f"Select a user to view (Day {day_idx+1})",
                    options=list(range(len(user_labels))),
                    format_func=lambda i: user_labels[i],
                    key=f"user_selectbox_day_{day_idx+1}",
                )
                agent_result = round_results[selected_idx]
                agent = agent_result["agent"]
                feed = agent_result["feed"]
                observations = agent_result["observations"]
                engagements = agent_result["engagements"]
                with st.expander("Profile", expanded=False):
                    st.markdown(agent.profile.get_profile_description())
                st.markdown(f"### Feed for User {selected_idx+1} on Day {day_idx+1}")
                for i, post in enumerate(feed.posts):
                    with st.expander(f"Feed Post #{i+1}"):
                        st.markdown(f"**Post:** {post.text}")
                        st.markdown(
                            f"**Agent Thoughts:** {observations[i].observation if observations and i < len(observations) else ''}"
                        )
                        actions = (
                            engagements[i].engagement
                            if engagements and i < len(engagements) and engagements[i]
                            else {}
                        )
                        if actions:
                            st.markdown("**Actions:**")
                            for action, rationale in actions.items():
                                st.markdown(f"- **{action.capitalize()}**: {rationale}")
                        else:
                            st.markdown("**Actions:** None")
                st.markdown("---")

    # Network Summary Section
    st.header("Network Summary")
    social_network_component()
    analyze_network_component()

    # Total Simulation Metrics Section
    st.header("Total Simulation Metrics")
    st.write("[Stub] Overall simulation metrics will be shown here.")

    # Export Section
    st.header("Export Simulation")
    st.button("Export (stub)")
