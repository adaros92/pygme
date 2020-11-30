import pytest
import random

from pygme.utils import validation


def test_validate_user_input():
    """ Tests utils.validation.validate_user_input """
    # Normal operation
    input_value = 1
    input_type = str
    assert validation.validate_user_input("test_int", input_value, input_type) == "1"
    input_value = "1"
    input_type = int
    assert validation.validate_user_input("test_int", input_value, input_type) == 1
    # Invalid input
    input_value = "some_string"
    input_type = int
    with pytest.raises(ValueError):
        validation.validate_user_input("test_string", input_value, input_type)


def test_validate_grid_index():
    """ Tests utils.validation.validate_grid_index """
    # Normal operation
    for _ in range(100):
        random_grid_length = random.randint(1, 50)
        random_grid_width = random.randint(1, 50)
        random_x_coordinate = random.randint(-100, 100)
        random_y_coordinate = random.randint(-100, 100)
        valid_grid_index = validation.validate_grid_index(
            random_grid_length, random_grid_width, random_x_coordinate, random_y_coordinate)
        if random_x_coordinate < 0 or random_y_coordinate < 0:
            assert not valid_grid_index
        elif random_x_coordinate >= random_grid_length or random_y_coordinate >= random_grid_width:
            assert not valid_grid_index
        else:
            assert valid_grid_index
