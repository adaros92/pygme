import pytest
from pygme.battleship import player, ships, game


def test_place_fleet():
    """ Tests battleship.ships.Ship.is_destroyed """
    for _ in range(pytest.large_iteration_count):
        board_width, board_length = 20, 20
        # Initialize random ships
        game_board = game.BattleshipGame.construct_board(board_length, board_width)
        ship_fleet = ships.ShipFleet(pytest.battleship_test_config)
        players = [player.BattleshipPlayer() for _ in range(2)]
        players[0].computer = False
        players[1].computer = True
        human_player, computer_player = players[0], players[1]
        computer_player.place_ships(ship_fleet, game_board)
