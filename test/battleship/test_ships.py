import copy
import pytest
import random

from pygme.battleship import ships
from pygme.utils import space


# Util functions for ships testing
def _initialize_random_ships() -> list:
    # Initialize random ships
    eligible_types = ["destroyer", "submarine", "patrol"]
    corresponding_size = [3, 3, 2]
    ships_return_collection = []
    for _ in range(random.randint(1, pytest.small_iteration_count)):
        random_index = random.randint(0, len(eligible_types) - 2)
        random_ship_type = eligible_types[random_index]
        random_ship_size = corresponding_size[random_index]
        ship_object = ships.Ship(random_ship_type, random_ship_size)
        ships_return_collection.append(ship_object)
    return ships_return_collection


def _place_ship(ship: ships.Ship) -> None:
    """ Place a given ship on a hypothetical board for testing """
    board_width, board_length = 20, 20
    starting_coordinate = space.get_coordinates_between_limits(board_width, board_length)
    direction = space.get_random_directions(list(["down", "right", "up", "left"]), 1)[0]
    # Retrieve the coordinates based random starting location of ships
    coordinates = space.get_contiguous_coordinates(starting_coordinate, direction, ship.size)
    ship.place_ship(coordinates)


# Test functions
def test_is_ship_destroyed():
    """ Tests battleship.ships.Ship.is_destroyed method """
    for _ in range(pytest.large_iteration_count):
        ship_object = _initialize_random_ships()[0]
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


def test_ship_is_hit():
    """ Tests battleship.ships.ShipFleet.ship_is_hit method """
    fleet = ships.ShipFleet(config=pytest.battleship_test_config)
    for ship_name, ship in fleet.items():
        _place_ship(ship)
        for coordinate in ship.coordinates:
            ship.take_damage(coordinate)
            assert fleet.ship_is_hit(coordinate)


def test_accept_attack():
    """ Tests battleship.ships.ShipFleet.accept_attack and is_destroyed methods """
    fleet = ships.ShipFleet(config=pytest.battleship_test_config)
    assert not fleet.is_destroyed()
    for ship_name, ship in fleet.items():
        _place_ship(ship)
        for coordinate in ship.coordinates:
            # Freshly placed ships will not have any destroyed coordinates
            assert coordinate not in ship.destroyed_coordinates
            fleet.accept_attack(coordinate)
            # After an attack on the fleet though there will be destroyed coordinates
            assert coordinate in ship.destroyed_coordinates
        assert len(ship.destroyed_coordinates) == len(ship.coordinates)
    # All coordinates were attacked above so the fleet should be destroyed now
    assert fleet.is_destroyed()


def test_print():
    """ Tests battleship.ships.ShipFleet._print method """
    fleet = ships.ShipFleet(config=pytest.battleship_test_config)
    repr_print_result = fleet._print(repr)
    str_print_result = fleet._print(str)
    assert isinstance(repr_print_result, str) and isinstance(str_print_result, str)
    assert repr(fleet) == repr_print_result and str(fleet) == str_print_result


def test_unique_ship_representations():
    """ Tests battleship.ships.ShipFleet.unique_ship_representations method """
    fleet = ships.ShipFleet(config=pytest.battleship_test_config)
    unique_representation_characters = set()
    for ship_name, ship in fleet.items():
        unique_representation_characters.add(ship.representation)
    assert fleet.unique_ship_representations == unique_representation_characters
