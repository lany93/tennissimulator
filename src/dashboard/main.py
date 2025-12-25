import streamlit as st
from src.dashboard.util.session_state import initialize_session_state

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to Streamlit! 👋")

st.sidebar.success("Select a demo above.")

# Initialize session state
initialize_session_state()


# Introduction
st.markdown(
    """
    Tennis Simulator Dashboard is an interactive web application built with Streamlit that allows users to simulate tennis matches and tournaments. Users can customize various parameters, run simulations, and visualize the results through dynamic charts and tables.   
"""
)
