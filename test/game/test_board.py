import pytest
import random

from pygme.game import board


def test_create_board():
    """ Tests board.GameBoard._create_board method """
    # Test nominal operation with valid inputs
    for random_size in range(100):
        rand_length = random.randint(1, 10)
        rand_width = random.randint(1, 10)
        test_board = board.GameBoard(rand_length + 1, rand_width + 1).board
        assert len(test_board) == rand_length + 1
        assert len(test_board[0]) == rand_width + 1
    # Test invalid inputs
    with pytest.raises(AssertionError):
        _ = board.GameBoard(-1, 0)
    with pytest.raises(AssertionError):
        _ = board.GameBoard(1, -3)
    with pytest.raises(AssertionError):
        _ = board.GameBoard(0, 0)
