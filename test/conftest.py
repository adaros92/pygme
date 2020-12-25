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

