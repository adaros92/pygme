from pygme.battleship import player, ships, game


BATTLESHIP_TEST_CONFIG = {
    "ship_types": ["carrier", "battleship", "destroyer", "submarine", "patrol"],
    "size_by_type": {
      "carrier": 5, "battleship": 4, "destroyer": 3, "submarine": 3, "patrol": 2
    }
  }


def test_place_fleet():
    """ Tests battleship.ships.Ship.is_destroyed """
    for _ in range(25):
        board_width, board_length = 20, 20
        # Initialize random ships
        game_board = game.BattleshipGame.construct_board(board_length, board_width)
        ship_fleet = ships.ShipFleet(BATTLESHIP_TEST_CONFIG)
        players = [player.BattleshipPlayer() for _ in range(2)]
        players[0].computer = False
        players[1].computer = True
        human_player, computer_player = players[0], players[1]
        computer_player.place_ships(ship_fleet, game_board)
