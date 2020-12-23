import copy
import pytest
import random

from pygme.battleship import ships


def test_is_ship_destroyed():
    """ Tests battleship.ships.Ship.is_destroyed """
    for _ in range(pytest.large_iteration_count):
        # Initialize random ships
        eligible_types = ["destroyer", "submarine", "patrol"]
        corresponding_size = [3, 3, 2]
        random_index = random.randint(0, len(eligible_types)-2)
        random_ship_type = eligible_types[random_index]
        random_ship_size = corresponding_size[random_index]
        ship_object = ships.Ship(random_ship_type, random_ship_size)
        # At the beginning the ship will be fully functional
        assert not ship_object.is_destroyed()
        assert not ship_object.destroyed and not ship_object.placed
        # A fraction of bombed segments will not make the ship destroyed
        random_coordinates = [
            (random.randint(0, pytest.large_iteration_count), random.randint(0, pytest.large_iteration_count))
            for x in range(pytest.small_iteration_count)]
        ship_object.coordinates = set(random_coordinates)
        random.shuffle(random_coordinates)
        destroyed_coordinates = random_coordinates[:random.randint(1, max(len(random_coordinates) - 5, 1))]
        ship_object.destroyed_coordinates = set(destroyed_coordinates)
        assert not ship_object.is_destroyed() and not ship_object.destroyed
        # Only when all coordinates have been bombed will the ship be destroyed
        ship_object.destroyed_coordinates = set(copy.deepcopy(random_coordinates))
        assert ship_object.is_destroyed() and ship_object.destroyed

