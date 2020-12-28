import pytest
import random

from pygme.game import player
from pygme.battleship import game, board


@pytest.fixture
def mock_game_input(monkeypatch) -> None:
    def mock_get_user_input(*args, **kwargs) -> dict:
        """ mocks game.BattleshipGame _get_user_input method """
        return {"board_width": 20, "board_length": 20, "difficulty": "normal"}

    def mock_board_toggle_input(*args, **kwargs) -> str:
        return "b"

    monkeypatch.setattr(game.BattleshipGame, "_get_user_input", mock_get_user_input)
    monkeypatch.setattr(game.BattleshipGame, "_get_toggle_input", mock_board_toggle_input)


def test_assign_human_player():
    """ Tests _assign_human_player method in base Game class """
    for _ in range(pytest.small_iteration_count):
        # Start a test game and assign and create a random number of players
        test_game = game.BattleshipGame(config=pytest.battleship_test_config)
        test_game.number_of_players = random.randint(1, pytest.large_iteration_count)
        test_game.players = [player.Player(
            board.BattleshipBoard(pytest.large_iteration_count, pytest.large_iteration_count))
            for player_idx in range(test_game.number_of_players)]
        # Assign exactly one human player among the list of players
        test_game._assign_human_player()
        count_of_computers, count_of_humans = 0, 0
        for player_obj in test_game.players:
            if player_obj.computer:
                count_of_computers += 1
            elif not player_obj.computer:
                count_of_humans += 1
        # The number of players registered in the game should equal to the number assigned and there should be 1 human
        assert count_of_humans + count_of_computers == test_game.number_of_players and count_of_humans == 1


def test_player_handling():
    """ Tests _next_player and _other_players methods in base Game class """
    for _ in range(pytest.small_iteration_count):
        # Start a test game and assign and create a random number of players
        test_game = game.BattleshipGame(config=pytest.battleship_test_config)
        test_game.number_of_players = random.randint(1, pytest.large_iteration_count)
        test_game.players = [player.Player(
            board.BattleshipBoard(pytest.large_iteration_count, pytest.large_iteration_count))
            for player_idx in range(test_game.number_of_players)]
        for player_turn_iteration in range(4):
            seen_player_ids = set()
            # Keep getting the next player in line for as many players that exist in the game
            for player_idx in range(len(test_game.players)):
                generated_player = test_game._next_player()
                other_players = test_game._other_players()
                assert generated_player not in other_players and len(other_players) + 1 == test_game.number_of_players
                seen_player_ids.add(generated_player.player_id)
            # Ensure each player is retrieved at least once
            assert len(seen_player_ids) == len(test_game.players)


def test_print_result():
    """ Tests print_result method in base Game class """
    for _ in range(pytest.small_iteration_count):
        # Start a test game and assign and create a random number of players
        test_game = game.BattleshipGame(config=pytest.battleship_test_config)
        test_game.number_of_players = random.randint(1, pytest.large_iteration_count)
        test_game.players = [player.Player(
            board.BattleshipBoard(pytest.large_iteration_count, pytest.large_iteration_count))
            for player_idx in range(test_game.number_of_players)]
        test_game.players[0].winner = True
        # Ensure printing results doesn't raise exception under different random scenarios
        test_game.print_result()


def test_initialize(mock_game_input):
    """ Tests _initialize method in BattleShip game class """
    for _ in range(pytest.large_iteration_count):
        # Start a test game and assign and create a random number of players
        test_game = game.BattleshipGame(config=pytest.battleship_test_config)
        test_game._initialize()
        # Ensure boards/fleets created successfully and difficulty correctly captures after game initialization
        assert (test_game.difficulty == "normal" and len(test_game.boards) == len(test_game.players) and
                len(test_game.ship_fleets) == len(test_game.players))
        for player_id, game_board in test_game.boards.items():
            assert game_board.width == 20 and game_board.length == 20
        for player_id, fleet in test_game.ship_fleets.items():
            assert len(fleet) > 0
