import pytest
import random

from pygme.game import player
from pygme.battleship import game


def test_assign_human_player():
    """ Tests _assign_human_player method in base Game class """
    for _ in range(pytest.large_iteration_count):
        # Start a test game and assign and create a random number of players
        test_game = game.BattleshipGame(config=pytest.battleship_test_config)
        test_game.number_of_players = random.randint(1, pytest.large_iteration_count)
        test_game.players = [player.Player() for player_idx in range(test_game.number_of_players)]
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
    for _ in range(pytest.large_iteration_count):
        # Start a test game and assign and create a random number of players
        test_game = game.BattleshipGame(config=pytest.battleship_test_config)
        test_game.number_of_players = random.randint(1, pytest.large_iteration_count)
        test_game.players = [player.Player() for player_idx in range(test_game.number_of_players)]
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
    for _ in range(pytest.large_iteration_count):
        # Start a test game and assign and create a random number of players
        test_game = game.BattleshipGame(config=pytest.battleship_test_config)
        test_game.number_of_players = random.randint(1, pytest.large_iteration_count)
        test_game.players = [player.Player() for player_idx in range(test_game.number_of_players)]
        test_game.players[0].winner = True
        # Ensure printing results doesn't raise exception under different random scenarios
        test_game.print_result()