import pytest
import random
import string

from pygme.hangman import game
from pygme.utils.dictionary import Word


@pytest.fixture
def mock_hangman_input(monkeypatch) -> None:
    def mock_get_user_input(*args, **kwargs) -> dict:
        """ mocks game.Hangman _get_user_input method """
        return {"difficulty": "normal"}

    def mock_get_guess_input(*args, **kwargs) -> str:
        """ Mocks game.Hangman _get_guess_input method by returning a random character """
        return random.choice([char for char in string.ascii_letters])

    monkeypatch.setattr(game.HangmanGame, "_get_user_input", mock_get_user_input)
    monkeypatch.setattr(game.HangmanGame, "_get_guess_input", mock_get_guess_input)


def test_initialization(mock_hangman_input):
    """ Tests hangman.game._initialize method """
    test_game = game.HangmanGame(pytest.hangman_test_config)
    test_game._initialize()
    # When first starting a game of Hangman the noose will not be completely full
    assert not test_game.noose.is_complete()
    components_on_grid = set()
    # Test starting noose display on board
    for component in test_game.noose.noose_components:
        if component["displayed"]:
            components_on_grid.add(repr(component["part"]))
            # Ensure that if a component is supposed to be displayed that the board has been refreshed with it
            assert test_game.board.board[component["x_index"]][component["y_index"]] == repr(component["part"])
    for column in test_game.board.board:
        for element in column:
            # Ensure that no other elements beyond the displayed parts and the empty square character are on the board
            assert element == " " or element in components_on_grid


def test_has_won(mock_hangman_input):
    """ Tests hangman.game._has_won method """
    test_game = game.HangmanGame(pytest.hangman_test_config)
    test_game.word = Word("thiSisAteEst")
    test_game.guessed_characters = set("thisae")
    assert test_game._has_won()
    test_game.guessed_characters = set("thi")
    assert not test_game._has_won()


def test_run(mock_hangman_input):
    test_game = game.HangmanGame(pytest.hangman_test_config)
    test_game.run()
    assert test_game._is_game_over()
    assert test_game._has_won() or test_game._man_died()

