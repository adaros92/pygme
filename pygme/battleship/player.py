from pygme.battleship import ships, board
from pygme.game import player
from pygme.utils import space, validation


class BattleshipPlayer(player.Player):

    def __init__(self, computer=True):
        super().__init__(computer=computer)

    def guess(self, game_board: board.BattleshipBoard) -> tuple:
        """ Each player will guess the other's ships' locations and attack them one at a time

        :param game_board - the board where ships are currently located
        :returns a tuple containing the X and Y coordinates of the square to attack
        """
        # Accept input from player if they're not the computer
        input_valid = False
        coordinate = None
        if not self.computer:
            while not input_valid:
                try:
                    x_coordinate_guess = int(input("Enter the x-coordinate of the square to attack:"))
                    y_coordinate_guess = int(input("Enter the y-coordinate of the square to attach:"))
                    coordinate = (x_coordinate_guess, y_coordinate_guess)
                except ValueError:
                    print("Individual coordinate components must be single integers")
                    continue
                if space.are_coordinates_between_limits(coordinate, game_board.width, game_board.length):
                    input_valid = True
        # Follow guessing algorithm if computer
        else:
            # TODO Implement a smart guessing algorithm
            coordinate = space.get_coordinates_between_limits(game_board.width, game_board.length)
        return coordinate

    @staticmethod
    def _validate_ship_placement(coordinates: list, game_board: board.BattleshipBoard) -> None:
        """ Validates that the given coordinates for ship placement on the given board are valid

        :param coordinates - a list of x and y coordinate tuples to check the validity of
        :param game_board - the board object to place the given coordinates in
        """
        for coordinate in coordinates:
            if len(coordinate) != 2:
                raise ValueError("A coordinate must be a tuple consisting of X and Y integers")
            if not space.are_coordinates_between_limits(coordinate, game_board.width, game_board.length):
                raise ValueError("The location of the ship is not within the boundaries of the grid")
            if not game_board.is_square_clear(coordinate):
                raise ValueError("The location of the ship overlaps another ship")

    def _place_ship(self, ship: ships.Ship, game_board: board.BattleshipBoard) -> None:
        """ Place a given ship on the given board

        Placement works by picking a starting coordinate and generating contiguous slots on the board from that starting
        location in one of two possible directions - right or down

        :param ship - the ship to place on the board
        :param game_board - the board to place the ship on
        """
        ship_placement_ok = False
        ship_directions = {"right", "down"}
        # Keep trying to place the ship until it doesn't overlap with anything that's currently on the board
        while not ship_placement_ok:
            try:
                # The human player will provide the coordinates for each ship
                if not self.computer:
                    # Receive input from human user on where and how to place the ship
                    print("Place the {0} ship of size {1}".format(ship.ship_type, ship.size))
                    direction = input("Enter either right or down for the direction the ship will face: ")
                    validation.validate_out_of_possible_options(direction, ship_directions)
                    starting_coordinate = input(
                        "Enter coordinate of left-most or top-most square to place ship in (x,y):")
                    starting_coordinate_list = starting_coordinate.replace(
                        "(", "").replace(")", "").replace(" ", "").split(",")
                    starting_coordinate = tuple([int(x) for x in starting_coordinate_list])
                    self._validate_ship_placement([starting_coordinate], game_board)
                # The computer will just pick at random until the placement is successful
                else:
                    board_width, board_length = game_board.width, game_board.length
                    starting_coordinate = space.get_coordinates_between_limits(board_width, board_length)
                    direction = space.get_random_directions(list(ship_directions), 1)[0]
                # Retrieve the coordinates based on input or random starting location of ships
                coordinates = space.get_contiguous_coordinates(starting_coordinate, direction, ship.size)
                # Raise exception if any of the ships go beyond the board or if they overlap others
                self._validate_ship_placement(coordinates, game_board)
                # Let ship object know that it is placed on a grid
                ship.place_ship(coordinates)
                ship_placement_ok = True
                # Update the board with the new ship
                game_board.place_ship(ship)
            except ValueError as e:
                # Let human player know what went wrong with their placement and retry
                if not self.computer:
                    print(e)
                continue

    def place_ships(self, fleet: ships.ShipFleet, game_board: board.BattleshipBoard) -> None:
        """ Places each ship in the given fleet on the given board

        :param fleet - the fleet containing ships to be placed on the board
        :param game_board - the board to place the ships on
        """
        for ship_name, ship in fleet.items():
            self._place_ship(ship, game_board)
