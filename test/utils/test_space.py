import random

from pygme.utils import space


def test_get_coordinates_between_limits():
    """ Tests utils.space.get_coordinates_between_limits function """
    for _ in range(1000):
        grid_width = random.randint(1, 100)
        grid_length = random.randint(1, 100)
        coordinates = space.get_coordinates_between_limits(grid_width=grid_width, grid_length=grid_length)
        assert 0 <= coordinates[0] <= grid_length - 1
        assert 0 <= coordinates[1] <= grid_width - 1
