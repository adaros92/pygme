import pytest


def pytest_configure():
    """ Specifies pytest configurations to use across tests """
    # General pytest constants
    pytest.small_iteration_count = 25
    pytest.large_iteration_count = 100
    pytest.very_large_iteration_count = 100000
    # Common test objects for battleship
    pytest.ship_types = ["carrier", "battleship", "destroyer", "submarine", "patrol"]
    pytest.size_by_type = {"carrier": 5, "battleship": 4, "destroyer": 3, "submarine": 3, "patrol": 2}
    pytest.battleship_test_config = {
        "ship_types": ["carrier", "battleship", "destroyer", "submarine", "patrol"],
        "size_by_type": {"carrier": 5, "battleship": 4, "destroyer": 3, "submarine": 3, "patrol": 2},
        "required_inputs": {"board_width": "int", "board_length": "int", "difficulty": "str"},
        "number_of_players": 2
    }
    pytest.hangman_test_config = {
        "dictionary_filename": "dictionary.txt", "required_inputs": {"difficulty": "str"},
        "number_of_players": 1, "board_width": 10, "board_length": 10,
        "word_sizes_by_difficulty": {
          "easy": {"min_word_length": 2, "max_word_length": 4},
          "normal": {"min_word_length": 5, "max_word_length": 8},
          "hard": {"min_word_length": 9, "max_word_length": 100}
        }
    }
    pytest.default_dictionary_config = {"dictionary_filename": "dictionary.txt"}

