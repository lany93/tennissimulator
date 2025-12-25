import logging
import random
from typing import Any
from src.tennis_simulator.tennis_scoring.tennis_score import TennisScore


class Simulator:
    """Class to simulate tennis matches and gather statistics."""

    def __init__(self, winrate_player_1: float = 0.5) -> None:
        self._winrate_player_1 = winrate_player_1  # Default win rate for player 1
        self.statistics: dict[str, Any] = {
            "number_of_matches": 0,
            "player_1_wins": 0,
            "player_2_wins": 0,
            "player_1_total_points_won": 0,
            "player_2_total_points_won": 0,
            "results": [],
            "simulated_point_win_rate_player_1": [],
        }

    def _simulate_game(self) -> TennisScore:
        """Run a simulation of a tennis game.

        Returns:
            TennisScore: The final score of the simulated tennis game.
        """
        tennis_score = TennisScore()

        # Run as long as there is no winner
        while not tennis_score.winner:
            winner = self._simulate_points(win_rate_player_1=self._winrate_player_1)
            tennis_score._update_score(winner)
        logging.info("Simulation complete.")
        return tennis_score

    def _simulate_points(self, win_rate_player_1: float) -> str:
        """Simulate win or loss based on the given win rate.

        Args:
            win_rate_player_1 (float): Win rate of player 1 (between 0 and 1).
            tennis_score (TennisScore): Current tennis score object.

        Returns:
            str:  Identifier of the winning player ("player_1" or "player_2").
        """
        if random.random() < win_rate_player_1:
            self.statistics["player_1_total_points_won"] += 1
            return "player_1"

        self.statistics["player_2_total_points_won"] += 1
        return "player_2"

    def _gather_match_result(self, tennis_score: TennisScore) -> None:
        """Gather statistics from the completed tennis score."""
        if tennis_score.winner == "player_1":
            self.statistics["player_1_wins"] += 1
        else:
            self.statistics["player_2_wins"] += 1
        # TODO: Get points per match and games per match. How many Deuces and so on.
        self.statistics["results"].append(tennis_score.match_result())

    def run_simulation(self, number_of_simulations: int = 10) -> None:
        """Run the full tennis match simulation."""

        # Reset statistics before starting simulations
        self._reset_statistics()

        # Run the specified number of simulations
        for i in range(number_of_simulations):
            logging.info(f"Starting simulation {i + 1}/{number_of_simulations}.")
            tennis_score = self._simulate_game()
            logging.info(
                f"Simulation {i + 1} complete. Winner: {tennis_score.winner}. Final Score: {tennis_score.match_result()}."
            )
            self._gather_match_result(tennis_score)
            self.statistics["simulated_point_win_rate_player_1"].append(
                tennis_score.score["player_1_total_points_won"]
                / (
                    tennis_score.score["player_1_total_points_won"]
                    + tennis_score.score["player_2_total_points_won"]
                )
            )  # TODO: this should be on match level meaning after each match on not on simulation level

        self.statistics["number_of_matches"] = number_of_simulations

    def _reset_statistics(self) -> None:
        """Reset the statistics to initial state."""
        self.statistics = {
            "number_of_matches": 0,
            "player_1_wins": 0,
            "player_2_wins": 0,
            "player_1_total_points_won": 0,
            "player_2_total_points_won": 0,
            "results": [],
            "simulated_point_win_rate_player_1": [],
        }
