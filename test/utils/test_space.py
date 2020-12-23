import pytest
import random

from pygme.utils import space


def test_get_coordinates_between_limits():
    """ Tests utils.space.get_coordinates_between_limits function """
    for _ in range(pytest.very_large_iteration_count):
        grid_width = random.randint(1, pytest.large_iteration_count)
        grid_length = random.randint(1, pytest.large_iteration_count)
        coordinates = space.get_coordinates_between_limits(grid_width=grid_width, grid_length=grid_length)
        assert 0 <= coordinates[0] <= grid_length - 1
        assert 0 <= coordinates[1] <= grid_width - 1


def test_are_coordinates_between_limits():
    """ Tests utils.space.are_coordinates_between_limits function """
    grid_width = 25
    grid_length = 10
    coordinates = (5, 10)
    assert space.are_coordinates_between_limits(coordinates, grid_length=grid_length, grid_width=grid_width)
    grid_width = 10
    assert not space.are_coordinates_between_limits(coordinates, grid_length=grid_length, grid_width=grid_width)
    for _ in range(100):
        grid_width = random.randint(1, pytest.large_iteration_count)
        grid_length = random.randint(1, pytest.large_iteration_count)
        coordinates = space.get_coordinates_between_limits(grid_width=grid_width, grid_length=grid_length)
        assert space.are_coordinates_between_limits(coordinates, grid_width, grid_length)


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
    for _ in range(pytest.large_iteration_count):
        random_coordinates = (
            random.randint(-pytest.large_iteration_count, pytest.large_iteration_count),
            random.randint(-pytest.large_iteration_count, pytest.large_iteration_count)
        )
        random_size = random.randint(5, pytest.large_iteration_count)
        random_direction = ["right", "left", "up", "down"][random.randint(0, 3)]
        result_coordinates = space.get_contiguous_coordinates(random_coordinates, random_direction, random_size)
        assert space.are_contiguous_coordinates(result_coordinates)
