import pytest
import random

from pygme.battleship import board, ships


def test_place_ship():
    """ Tests board.BattleshipBoard.place_ship method """
    for scenario in range(pytest.large_iteration_count):
        # Get random ship
        random_ship_type = pytest.ship_types[random.randint(0, len(pytest.ship_types) - 1)]
        ship_size = pytest.size_by_type[random_ship_type]
        ship = ships.Ship(random_ship_type, ship_size)
        # Assign random coordinates to that ship
        coordinates = [
            (random.randint(0, pytest.large_iteration_count), random.randint(0, pytest.large_iteration_count))]
        # Place the ship
        ship.place_ship(coordinates)
        game_board = board.BattleshipBoard(200, 200)
        game_board.place_ship(ship)
        # Ensure the board reflects the newly placed ship
        for coordinate in ship.coordinates:
            assert game_board.board[coordinate[0]][coordinate[1]] == ship.representation


def test_attack():
    """ Tests board.BattleshipBoard.attack method """
    for scenario in range(pytest.large_iteration_count):
        pass
