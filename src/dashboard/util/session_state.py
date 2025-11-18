"""Session state utilities for the dashboard."""

import streamlit as st


def initialize_session_state():
    # Initialize default session state values
    if "p1_point_win_rate" not in st.session_state:
        st.session_state.p1_point_win_rate = 0.6
