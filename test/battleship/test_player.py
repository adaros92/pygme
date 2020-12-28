import pytest

from pygme.battleship import player, ships, game
from pygme.utils import space


@pytest.fixture
def mock_player_input(monkeypatch) -> None:

    def mock_get_coordinate_from_input(*args, **kwargs) -> tuple:
        """ mocks player.BattleshipPlayer._get_coordinate_from_input method """
        return 0, 0

    monkeypatch.setattr(player.BattleshipPlayer, "_get_coordinate_from_input", mock_get_coordinate_from_input)


def _initialize_resources():
    """ Initializes common Battleship player test resources """
    board_width, board_length = 20, 20
    # Initialize random ships
    game_board = game.BattleshipGame.construct_board(board_length, board_width)
    ship_fleet = ships.ShipFleet(pytest.battleship_test_config)
    # Create players
    players = [player.BattleshipPlayer(game_board) for _ in range(2)]
    players[0].computer = False
    players[1].computer = True
    human_player, computer_player = players[0], players[1]
    computer_player.place_ships(ship_fleet)
    return players, ship_fleet, game_board


def test_place_fleet():
    """ Tests player.place_ships method """
    for _ in range(pytest.large_iteration_count):
        _, ship_fleet, _ = _initialize_resources()
        for ship_name, ship in ship_fleet.items():
            assert ship.placed and not ship.destroyed


def test_guess(mock_player_input):
    """ Tests player.guess method """
    for _ in range(pytest.large_iteration_count):
        players, _, game_board = _initialize_resources()
        for battleship_player in players:
            guess = battleship_player.guess({
                "coordinate": (0,0),
                "successful_hit": False,
                "ship_destroyed": False,
                "already_hit": False
            })
            assert space.are_coordinates_between_limits(guess, game_board.width, game_board.length)
