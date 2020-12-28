import pytest
import random

from pygme.utils import space


def test_get_coordinates_between_limits():
    """ Tests utils.space.get_coordinates_between_limits function """
    for _ in range(pytest.small_iteration_count):
        grid_width = random.randint(1, pytest.large_iteration_count)
        grid_length = random.randint(1, pytest.large_iteration_count)
        coordinates = space.get_coordinates_between_limits(grid_width=grid_width, grid_length=grid_length)
        assert 0 <= coordinates[0] <= grid_length - 1
        assert 0 <= coordinates[1] <= grid_width - 1
        exclusion_list = []
        for length in range(grid_length):
            for width in range(grid_width):
                exclusion_list.append((length, width))
        exclusion_set = set(exclusion_list[:-1])
        coordinates = space.get_coordinates_between_limits(
            grid_width=grid_width, grid_length=grid_length, exclusion_set=exclusion_set)
        assert coordinates == exclusion_list[-1]


def test_are_coordinates_between_limits():
    """ Tests utils.space.are_coordinates_between_limits function """
    grid_width = 25
    grid_length = 10
    coordinates = (5, 10)
    assert space.are_coordinates_between_limits(coordinates, grid_length=grid_length, grid_width=grid_width)
    grid_width = 10
    assert not space.are_coordinates_between_limits(coordinates, grid_length=grid_length, grid_width=grid_width)
    for _ in range(pytest.large_iteration_count):
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


def test_get_adjacent_coordinates():
    """ Tests utils.space.get_adjacent_coordinates function """
    for _ in range(pytest.large_iteration_count):
        random_coordinates = (
            random.randint(0, pytest.large_iteration_count - 1),
            random.randint(0, pytest.large_iteration_count - 1)
        )
        grid_width = pytest.large_iteration_count
        grid_length = pytest.large_iteration_count
        adjacent_coordinates = space.get_adjacent_coordinates(
            random_coordinates, grid_width, grid_length)
        # There can be at most 4 adjacent coordinates on a 2D grid and a minimum of 2 if grid is this size
        assert 2 <= len(adjacent_coordinates) <= 4
        adjacent_coordinates_list = [
            (random_coordinates[0] - 1, random_coordinates[1]),
            (random_coordinates[0] + 1, random_coordinates[1]),
            (random_coordinates[0], random_coordinates[1] - 1),
            (random_coordinates[0], random_coordinates[1] + 1),
        ]
        # Ensure only adjacent coordinates within grid bounds are returned from get_adjacent_coordinates function
        for expected_adjacent_coordinate in adjacent_coordinates_list:
            if space.are_coordinates_between_limits(expected_adjacent_coordinate, grid_width, grid_length):
                assert expected_adjacent_coordinate in adjacent_coordinates
            else:
                assert expected_adjacent_coordinate not in adjacent_coordinates
