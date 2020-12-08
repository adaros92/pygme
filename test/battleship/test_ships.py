import copy
import random

from pygme.battleship import ships


BATTLESHIP_TEST_CONFIG = {
    "ship_types": ["carrier", "battleship", "destroyer", "submarine", "patrol"],
    "size_by_type": {
      "carrier": 5, "battleship": 4, "destroyer": 3, "submarine": 3, "patrol": 2
    }
  }


def test_is_ship_destroyed():
    """ Tests battleship.ships.Ship.is_destroyed """
    for _ in range(25):
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
        random_coordinates = [(random.randint(0, 100), random.randint(0, 100)) for x in range(25)]
        ship_object.coordinates = set(random_coordinates)
        random.shuffle(random_coordinates)
        destroyed_coordinates = random_coordinates[:random.randint(1, max(len(random_coordinates) - 5, 1))]
        ship_object.destroyed_coordinates = set(destroyed_coordinates)
        assert not ship_object.is_destroyed() and not ship_object.destroyed
        # Only when all coordinates have been bombed will the ship be destroyed
        ship_object.destroyed_coordinates = set(copy.deepcopy(random_coordinates))
        assert ship_object.is_destroyed() and ship_object.destroyed


'''
def test_is_fleet_destroyed():
    """ Tests battleship.ships.ShipFleet.is_destroyed """
    for _ in range(25):
        # When the fleet is fresh then no ships are destroyed
        fleet = ships.ShipFleet(BATTLESHIP_TEST_CONFIG)
        assert not fleet.is_destroyed() and not fleet.destroyed
        # If any one ship is destroyed then the fleet remains
        fleet[BATTLESHIP_TEST_CONFIG["ship_types"][0]].destroyed = True
        assert not fleet.is_destroyed() and not fleet.destroyed
        # If all ships in the fleet are destroyed then so is the fleet
        for ship_type, ship in fleet.items():
            ship.destroyed = True
        assert fleet.is_destroyed() and fleet.destroyed
'''
