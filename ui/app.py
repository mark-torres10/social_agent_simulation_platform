"""
Main entrypoint for the Agent Simulation Platform UI (first pass, stub only).
Follows the plan in planning/3_ui_first_pass_planning.md.
"""

import streamlit as st

# Import stub components
from ui.components.config.agent_config import agent_config_component
from ui.components.config.simulation_config import simulation_config_component
from ui.components.network.social_network import social_network_component
from ui.components.analysis.analyze_network import analyze_network_component

st.set_page_config(page_title="AI Agent Simulation Platform", layout="wide")

st.title("AI Agent Simulation Platform")

# Agent Configuration Section
st.header("Agent Configuration")
agent_config_component()

# Simulation Configuration Section
st.header("Simulation Configuration")
simulation_config_component()

# Start Simulation Button
st.button("Start Simulation (stub)")

# Simulation View Section
st.header("Simulation View")

# Placeholder data for posts
stub_posts = [
    "Just had the best coffee ever! ☕️ #morningvibes",
    "Excited for the new season of my favorite show! 📺",
    "Anyone else struggling with productivity today? 😅",
]

# Use tabs for days
day_tabs = st.tabs([f"Day {i}" for i in range(1, 6)])
for day_idx, day_tab in enumerate(day_tabs, start=1):
    with day_tab:
        # Tabs for users within each day
        user_tabs = st.tabs([f"User {i}" for i in range(1, 3)])
        for user_idx, user_tab in enumerate(user_tabs, start=1):
            with user_tab:
                st.markdown(f"### Feed for User {user_idx} on Day {day_idx}")
                # Vertically stacked feed posts
                for i, post in enumerate(stub_posts):
                    with st.expander(f"Feed Post #{i+1}"):
                        st.markdown(f"**Post:** {post}")
                        st.markdown(
                            "**Agent Thoughts:** <the agent thought would go here>"
                        )
                        st.markdown("**Actions:** <the agent actions would go here>")
                st.markdown("---")

# User actions and opinion changes section
st.subheader("User Actions and Opinion Changes")
st.write("[Stub] User actions and opinion changes will be shown here.")

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
