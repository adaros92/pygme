

class Ship(object):

    def __init__(self, ship_type, size):
        self.ship_type = ship_type
        self.size = size
        self.coordinates = set()
        self.destroyed_coordinates = set()
        self.placed = False
        self.destroyed = False

    def __repr__(self):
        return "{0} of size {1} with coordinates {2}".format(self.ship_type, self.size, self.coordinates)

    def __str__(self):
        return "{0} of size {1}".format(self.ship_type, self.size)

    def is_destroyed(self) -> bool:
        self.destroyed = False
        coordinate_length, destroyed_length = len(self.coordinates), len(self.destroyed_coordinates)
        if coordinate_length > 0 and destroyed_length > 0 and len(self.coordinates - self.destroyed_coordinates) == 0:
            self.destroyed = True
        return self.destroyed


class ShipFleet(dict):

    def __init__(self, config: dict):
        self.destroyed = False
        assert "ship_types" in config and "size_by_type" in config
        ship_types = config.get("ship_types", set())
        size_by_type = config.get("size_by_type", {})
        super().__init__({
            ship_type: Ship(ship_type, size) for ship_type, size in size_by_type.items() if ship_type in ship_types
        })

    def is_destroyed(self) -> bool:
        self.destroyed = True
        for _, ship in self.items():
            ship_destroyed = ship.is_detroyed
            # If any one ship is still alive then the fleet is also still alive
            if not ship_destroyed:
                self.destroyed = False
        return self.destroyed

    def _print(self, print_function):
        return_str = "Ship fleet: "
        for _, ship in self.items():
            return_str += "{0}, ".format(print_function(ship))
        return return_str[:-2]

    def __repr__(self):
        return self._print(repr)

    def __str__(self):
        return self._print(str)
