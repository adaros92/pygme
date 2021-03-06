import pytest
import random

from pygme.game import board


def test_create_board():
    """ Tests board.GameBoard._create_board method """
    # Construct random boards under normal operation
    for _ in range(pytest.large_iteration_count):
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


def test_clear():
    """ Tests board.GameBoard.clear method """
    for _ in range(pytest.large_iteration_count):
        # Construct random board
        rand_length = random.randint(1, 100)
        rand_width = random.randint(1, 10)
        test_board = board.GameBoard(rand_length + 1, rand_width + 1, empty_square=0)
        # Fill the boards at random places
        for fill_iter in range(10):
            random_x_index = random.randint(0, rand_length - 1)
            random_y_index = random.randint(0, rand_width - 1)
            test_board.board[random_x_index][random_y_index] = '*'
        # Clear the board
        test_board.clear()
        # Ensure all squares are empty
        for column in test_board.board:
            assert sum(column) == 0


def test_refresh_board():
    """ Tests board.GameBoard.refresh method """
    test_board = board.GameBoard(1, 3)
    expected_board_1 = [["_", "*", "_"]]
    board_1_coordinates = [(0, 1), (-100, 23), (1000, -1000), (-1, 1)]
    test_board.refresh(board_1_coordinates, "*")
    assert expected_board_1 == test_board.board
    test_board = board.GameBoard(2, 4)
    expected_board_2 = [["_", "*", "_", "_"], ["*", "*", "*", "*"]]
    board_2_coordinates = [(0, 1), (1, 0), (1, 1), (1, 2), (1, 3), (100, 100), (-999, 1), (0, -1)]
    test_board.refresh(board_2_coordinates, "*")
    assert expected_board_2 == test_board.board
    test_board.clear()
    assert expected_board_2 != test_board.board
    board_2_coordinates = [(0, 1), (1, 0)]
    test_board.refresh(board_2_coordinates, "*")
    assert expected_board_2 != test_board.board


def test_is_square_clear():
    """ Tests board.GameBoard.is_square_clear method """
    for _ in range(pytest.large_iteration_count):
        # Construct random board
        rand_length = random.randint(1, 100)
        rand_width = random.randint(1, 10)
        test_board = board.GameBoard(rand_length + 1, rand_width + 1)
        random_coordinates = (random.randint(0, rand_length - 1), random.randint(0, rand_width - 1))
        assert test_board.is_square_clear(random_coordinates)
        test_board.board[random_coordinates[0]][random_coordinates[1]] = "*"
        assert not test_board.is_square_clear(random_coordinates)


def test_print_board():
    """ Tests board.GameBoard.print method """
    for _ in range(pytest.large_iteration_count):
        # Construct random board
        rand_length = random.randint(1, 100)
        rand_width = random.randint(1, 10)
        test_board = board.GameBoard(rand_length + 1, rand_width + 1)
        for i in range(100):
            random_coordinates = (random.randint(0, rand_length - 1), random.randint(0, rand_width - 1))
            test_board.refresh([random_coordinates], representation="*", clear_board=False)
        # Print board out to ensure no exception pops up
        test_board.print()
        test_board.print(include_reference=True)
