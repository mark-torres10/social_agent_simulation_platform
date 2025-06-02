"""
UI component stub for agent configuration (first pass).
"""

import streamlit as st


def agent_config_component():
    """Stub for agent configuration UI."""
    st.subheader("Number of Agents")
    num_agents = st.number_input(
        "Select number of agents", min_value=1, max_value=100, value=5
    )

    print(f"Number of agents: {num_agents}")

    st.subheader("Agent Personas")
    persona_options = ["Default", "Custom"]
    persona_choice = st.selectbox("Choose persona type", persona_options)
    if persona_choice == "Custom":
        st.text_area("Enter custom persona descriptions (one per line)")
    else:
        st.write("Using default personas.")

    st.subheader("Other Settings")
    st.write("[Stub] Additional agent configuration options will go here.")
