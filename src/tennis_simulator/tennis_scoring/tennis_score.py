from typing import Any


class TennisScore:
    """Class to represent and manage tennis scoring."""

    def __init__(
        self,
        score: dict[str, Any] = None,
        player_1_score_index: int = 0,
        player_2_score_index: int = 0,
    ) -> None:
        self.score = score or {
            "player_1": 0,
            "player_2": 0,
            "player_1_games": 0,
            "player_2_games": 0,
            "player_1_tiebreak_points": 0,
            "player_2_tiebreak_points": 0,
            "player_1_sets": [],
            "player_2_sets": [],
        }
        self.score_map = [0, 15, 30, 40, "Advantage", "Game"]
        self.player_1_score_index = player_1_score_index
        self.player_2_score_index = player_2_score_index

    def _update_score(self, player: str) -> None:
        """Update the score for the given player.

        Args:
            player (str): Identifier for the player ("player_1" or "player_2").
        """
        # TODO: Handle advantage and deuce scenarios
        if player == "player_1":
            self.player_1_score_index += 1
        elif player == "player_2":
            self.player_2_score_index += 1
        else:
            raise ValueError("Invalid player identifier")

        self.score["player_1"] = self.score_map[self.player_1_score_index]
        self.score["player_2"] = self.score_map[self.player_2_score_index]

        # Update game and set after score change
        self._update_game()
        self._update_set()

    def _update_game(self) -> None:
        """Check if it is a game."""
        # player 1 wins a game
        if (self.player_1_score_index == (len(self.score_map) - 1)) | (
            self.player_1_score_index == 4 and self.player_2_score_index <= 2
        ):
            self.score["player_1_games"] += 1
            self._reset_points_to_zero()
            return
        # Player 2 wins a game
        elif (self.player_2_score_index == (len(self.score_map) - 1)) | (
            self.player_2_score_index == 4 and self.player_1_score_index <= 2
        ):
            self.score["player_2_games"] += 1
            self._reset_points_to_zero()
            return

    def _reset_points_to_zero(self) -> None:
        """Reset points to zero after a game."""
        self.player_1_score_index = 0
        self.player_2_score_index = 0
        self.score["player_1"] = self.score_map[self.player_1_score_index]
        self.score["player_2"] = self.score_map[self.player_2_score_index]

    def _is_tiebreak(self) -> bool:
        """Check if it is a tiebreak."""
        if (self.score["player_1_games"] == 6) & (self.score["player_2_games"] == 6):
            return True
        return False

    def _reset_games_and_tiebreak_points(self) -> None:
        """Reset games and tiebreak points after a set."""
        self.score["player_1_games"] = 0
        self.score["player_2_games"] = 0
        self.score["player_1_tiebreak_points"] = 0
        self.score["player_2_tiebreak_points"] = 0

    def _update_set(self) -> None:
        """Check if it is a set."""
        # Check for tiebreak set win
        if self._is_tiebreak():
            if (
                abs(
                    self.score["player_1_tiebreak_points"]
                    - self.score["player_2_tiebreak_points"]
                )
                >= 2
            ):
                if self.score["player_1_tiebreak_points"] >= 7:
                    self.score["player_1_sets"].append(self.score["player_1_games"] + 1)
                    self.score["player_2_sets"].append(self.score["player_2_games"])
                    self._reset_games_and_tiebreak_points()
                    return
                elif self.score["player_2_tiebreak_points"] >= 7:
                    self.score["player_1_sets"].append(self.score["player_1_games"])
                    self.score["player_2_sets"].append(self.score["player_2_games"] + 1)
                    self._reset_games_and_tiebreak_points()
                    return
                return
            return
        # Regular set win
        elif abs(self.score["player_1_games"] - self.score["player_2_games"]) >= 2:
            if self.score["player_1_games"] >= 6:
                self.score["player_1_sets"].append(self.score["player_1_games"])
                self.score["player_2_sets"].append(self.score["player_2_games"])
                self._reset_games_and_tiebreak_points()
                return
            elif self.score["player_2_games"] >= 6:
                self.score["player_1_sets"].append(self.score["player_1_games"])
                self.score["player_2_sets"].append(self.score["player_2_games"])
                self._reset_games_and_tiebreak_points()
                return
            return
        return

    def _won_match(self) -> bool:
        """Check if a player won the match."""
        pass
