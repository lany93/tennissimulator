from typing import Any


class TennisScore:
    """Class to represent and manage tennis scoring."""

    def __init__(
        self,
        score: dict[str, Any] | None = None,
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
            "player_1_sets_won": 0,
            "player_2_sets_won": 0,
            "player_1_total_points_won": 0,
            "player_2_total_points_won": 0,
        }
        self.score_map = [0, 15, 30, 40, "Advantage", "Game"]
        self.player_1_score_index = player_1_score_index
        self.player_2_score_index = player_2_score_index
        self.best_of_sets = 3  # Default best of 3 sets
        self.winner: str | None = None

    def _nr_of_sets_to_win(self) -> int:
        """Calculate the number of sets required to win the match.

        Returns:
            int: Number of sets required to win.
        """
        return (self.best_of_sets // 2) + 1

    def _score_to_index(self, score: int) -> int:
        """Convert score to index in score map.

        Args:
            score (int): Current score of the player.

        Returns:
            int: Index in the score map.
        """
        if score in self.score_map:
            return self.score_map.index(score)
        raise ValueError("Invalid score value")

    def _update_score(self, player: str) -> None:
        """Update the score for the given player.

        Args:
            player (str): Identifier for the player ("player_1" or "player_2").
        """
        # Handle advantage and deuce scenarios
        if self._is_tiebreak():
            if player == "player_1":
                self.score["player_1_tiebreak_points"] += 1
            else:
                self.score["player_2_tiebreak_points"] += 1
        else:
            if self.score_map[self.player_1_score_index] == "Advantage":
                if player == "player_1":
                    self.player_1_score_index += 1
                elif player == "player_2":
                    self.player_1_score_index -= 1
            elif self.score_map[self.player_2_score_index] == "Advantage":
                if player == "player_1":
                    self.player_2_score_index -= 1
                elif player == "player_2":
                    self.player_2_score_index += 1
            else:
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
                    self.score["player_1_sets_won"] += 1
                    self._reset_games_and_tiebreak_points()
                    self._won_match()
                    return
                elif self.score["player_2_tiebreak_points"] >= 7:
                    self.score["player_1_sets"].append(self.score["player_1_games"])
                    self.score["player_2_sets"].append(self.score["player_2_games"] + 1)
                    self.score["player_2_sets_won"] += 1
                    self._reset_games_and_tiebreak_points()
                    self._won_match()
                    return
                return

            return
        # Regular set win
        elif abs(self.score["player_1_games"] - self.score["player_2_games"]) >= 2:
            if self.score["player_1_games"] >= 6:
                self.score["player_1_sets"].append(self.score["player_1_games"])
                self.score["player_2_sets"].append(self.score["player_2_games"])
                self.score["player_1_sets_won"] += 1
                self._reset_games_and_tiebreak_points()
                self._won_match()
                return
            elif self.score["player_2_games"] >= 6:
                self.score["player_1_sets"].append(self.score["player_1_games"])
                self.score["player_2_sets"].append(self.score["player_2_games"])
                self.score["player_2_sets_won"] += 1
                self._reset_games_and_tiebreak_points()
                self._won_match()
                return
            return
        return

    def _won_match(self) -> None:
        """Check if a player won the match."""
        if self.score["player_1_sets_won"] >= self._nr_of_sets_to_win():
            self.winner = "player_1"
        elif self.score["player_2_sets_won"] >= self._nr_of_sets_to_win():
            self.winner = "player_2"

    def match_result(self) -> str:
        """Convert the current score to a human-readable format."""
        if len(self.score["player_1_sets"]) != len(self.score["player_2_sets"]):
            raise ValueError("Sets length mismatch")

        result = ""
        for i in range(len(self.score["player_1_sets"])):
            result += (
                f"{self.score['player_1_sets'][i]}-{self.score['player_2_sets'][i]},"
            )
        return result
