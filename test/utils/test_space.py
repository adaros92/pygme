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


def test_are_contiguous_coordinates():
    """ Tests utils.space.are_contiguous_coordinates function """
    coordinates = [(0, 1), (1, 1), (2, 1)]
    assert space.are_contiguous_coordinates(coordinates)
    coordinates = [(0, 1), (1, 1), (1, 1)]
    assert not space.are_contiguous_coordinates(coordinates)
    coordinates = [(0, 1), (1, 2), (2, 1)]
    assert not space.are_contiguous_coordinates(coordinates)
    coordinates = [(0, 1), (0, 1), (0, 1)]
    assert not space.are_contiguous_coordinates(coordinates)
    coordinates = [(0, 1), (0, 2), (0, 3)]
    assert space.are_contiguous_coordinates(coordinates)


def test_get_contiguous_coordinates():
    """ Tests utils.space.get_contiguous_coordinates function """
    for _ in range(100):
        random_coordinates = (random.randint(-100, 100), random.randint(-100, 100))
        random_size = random.randint(5, 100)
        random_direction = ["right", "left", "up", "down"][random.randint(0, 3)]
        result_coordinates = space.get_contiguous_coordinates(random_coordinates, random_direction, random_size)
        assert space.are_contiguous_coordinates(result_coordinates)
