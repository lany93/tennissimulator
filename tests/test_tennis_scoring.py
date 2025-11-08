"""Tests for tennis scoring module."""

from typing import List
import pytest

from src.tennis_simulator.tennis_scoring.tennis_score import TennisScore


@pytest.fixture
def tennis_score():
    """Fixture to create a TennisScore instance."""
    score = {
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
    }
    return TennisScore(score=score)


@pytest.mark.parametrize(
    "player, score, expected_score",
    [
        pytest.param("player_1", [0, 0], [15, 0], id="Update Score Player 1"),
        pytest.param("player_2", [0, 0], [0, 15], id="Update Score Player 2"),
        pytest.param("player_2", [30, 40], [0, 0], id="Update Score Player 2 Game"),
        pytest.param("player_1", [40, 30], [0, 0], id="Update Score Player 1 Game"),
        pytest.param(
            "player_1",
            [40, 40],
            ["Advantage", 40],
            id="Update Score Player 1 Advantage",
        ),
    ],
)
def test_update_score(
    player: str, score: List[int], expected_score: List[int], tennis_score: TennisScore
):
    """Test updating score for player."""
    tennis_score.player_1_score_index = tennis_score._score_to_index(score[0])
    tennis_score.player_2_score_index = tennis_score._score_to_index(score[1])

    # Update score for the specified player
    tennis_score._update_score(player)
    assert tennis_score.score["player_1"] == expected_score[0]
    assert tennis_score.score["player_2"] == expected_score[1]


@pytest.mark.parametrize(
    "player, points_won, expected_games, expected_score",
    [
        pytest.param("player_1", 4, 1, 0, id="Update Games Player 1"),
        pytest.param("player_2", 5, 1, 15, id="Update Games Player 2"),
        pytest.param("player_2", 8, 2, 0, id="Update Games Player 2"),
    ],
)
def test_update_games(
    tennis_score: TennisScore,
    points_won: int,
    expected_games: int,
    expected_score: int,
    player: str,
):
    """Test updating games after a player wins a game."""
    # Simulate player 1 winning a game
    for _ in range(points_won):
        tennis_score._update_score(player=player)
    assert tennis_score.score[player + "_games"] == expected_games
    assert tennis_score.score[player] == expected_score


@pytest.mark.parametrize(
    "player_1_games, player_2_games",
    [
        pytest.param(4, 6, id="Set Player 2 - Standard"),
        pytest.param(7, 5, id="Set Player 1"),
        pytest.param(5, 7, id="Set Player 2"),
    ],
)
def test_update_set_standard(
    tennis_score: TennisScore,
    player_1_games: int,
    player_2_games: int,
):
    """Test updating sets after a player wins a set."""
    tennis_score.score["player_1_games"] = player_1_games
    tennis_score.score["player_2_games"] = player_2_games
    tennis_score._update_set()
    assert tennis_score.score["player_1_sets"] == [player_1_games]
    assert tennis_score.score["player_2_sets"] == [player_2_games]


@pytest.mark.parametrize(
    "player_1_tiebreak_points, player_2_tiebreak_points, expected",
    [
        pytest.param(7, 5, [[7], [6]], id="Tiebreak Player 1 Wins"),
        pytest.param(5, 7, [[6], [7]], id="Tiebreak Player 2 Wins"),
        pytest.param(10, 9, [[], []], id="Tiebreak - Extended"),
        pytest.param(5, 1, [[], []], id="Tiebreak - Not Finished"),
        pytest.param(0, 6, [[], []], id="Tiebreak - Not Finished"),
    ],
)
def test_update_set_tiebreak(
    tennis_score: TennisScore,
    player_1_tiebreak_points: int,
    player_2_tiebreak_points: int,
    expected: list[int],
):
    """Test updating sets after a player wins a tiebreak set."""
    tennis_score.score["player_1_games"] = 6
    tennis_score.score["player_2_games"] = 6
    tennis_score.score["player_1_tiebreak_points"] = player_1_tiebreak_points
    tennis_score.score["player_2_tiebreak_points"] = player_2_tiebreak_points
    tennis_score._update_set()
    assert tennis_score.score["player_1_sets"] == expected[0]
    assert tennis_score.score["player_2_sets"] == expected[1]
