"""Dashboard simulation page."""

import streamlit as st

from src.tennis_simulator.simulation.simulator import simulator


st.title("Tennis Match Simulator")

# Input: Player 1 point win rate
st.number_input(
    "Player 1 point win rate",
    min_value=0.0,
    max_value=1.0,
    value=0.65,
    step=0.01,
    key="p1_point_win_rate",
)

# Number of simulations
num_simulations = st.number_input(
    "Number of Simulations", min_value=1, key="num_simulations", value=1000, step=1
)

# Button to run simulation
if st.button("Run Simulation"):
    with st.spinner("Running simulations..."):
        # Initialize and run the simulator
        simulation = simulator(winrate_player_1=st.session_state.p1_point_win_rate)
        simulation.run_simulation(number_of_simulations=num_simulations)

        # Display results
        st.write(simulation.statistics)
