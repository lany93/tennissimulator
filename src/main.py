import logging

from tennis_simulator.simulation.simulator import simulator


# Constants
CONFIG_FOLDER_PATH = "config"
WINRATE_PLAYER_1 = 0.60

logger = logging.getLogger("main")


def main():
    # config = ConfigManager(CONFIG_FOLDER_PATH)
    # config.load_config()
    # print(config.get())
    # print("Hello from tennis-simulator!")
    # simulation = simulator(WINRATE_PLAYER_1)
    # tennis_score = simulation.simulate_game()
    # print(f"Winner: {tennis_score.winner}.")
    # print(f"Final Score: {tennis_score.score}.")
    # print(f"Match Result: {tennis_score.match_result()}.")
    # logging.info(f"Winner: {tennis_score.winner}.")
    # logging.info(f"Final Score: {tennis_score.score}.")

    simulation = simulator(WINRATE_PLAYER_1)
    simulation.run_simulation(number_of_simulations=10000)
    print(simulation.statistics)


if __name__ == "__main__":
    main()
