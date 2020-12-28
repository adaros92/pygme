import pytest
import random

from pygme.battleship import board, strategy
from pygme.utils import space


def test_hunt_target_strategy_guess():
    """ Tests strategy.HuntTargetStrategy.guess method """
    board_dimension = pytest.small_iteration_count
    game_board = board.BattleshipBoard(board_dimension, board_dimension)
    game_strategy = strategy.HuntTargetStrategy(game_board)
    coordinate_guess = space.get_coordinates_between_limits(board_dimension, board_dimension)
    max_target_length = 0
    for _ in range(pytest.small_iteration_count ** 3):
        successful_hit = random.choices([True, False], [.90, .10])[0]
        if not successful_hit:
            ship_destroyed = False
        else:
            ship_destroyed = random.choices([True, False], [.50, .50])[0]
        information = {
            "coordinate": coordinate_guess,
            "successful_hit": successful_hit,
            "ship_destroyed": ship_destroyed
        }
        previous_target_length = len(game_strategy.targets)
        coordinate_guess = game_strategy.guess(information)
        max_target_length = max(previous_target_length, max_target_length)
        if ship_destroyed:
            assert not game_strategy.targets
    # Ensure that eventually all squares are guessed
    assert max_target_length >= 3 and len(game_strategy.already_guessed) == pytest.small_iteration_count ** 2
