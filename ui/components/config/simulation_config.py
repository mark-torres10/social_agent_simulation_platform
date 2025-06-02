"""
UI component stub for simulation configuration (first pass).
"""

import streamlit as st


def simulation_config_component():
    """Stub for simulation configuration UI."""
    st.subheader("Number of Turns")
    num_turns = st.number_input(
        "Select number of turns", min_value=1, max_value=100, value=10
    )

    print(f"Number of turns: {num_turns}")

    st.subheader("Other Simulation Parameters")
    st.write("[Stub] Additional simulation configuration options will go here.")
