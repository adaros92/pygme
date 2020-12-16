from pygme.battleship import ships, board
from pygme.game import player
from pygme.utils import space, validation


class BattleshipPlayer(player.Player):

    def __init__(self, computer=False):
        super().__init__(computer=computer)

    def guess(self, game_board: board.BattleshipBoard) -> tuple:
        """ Each player will guess the other's ships' locations """
        # Accept input from player if they're not the computer
        input_valid = False
        coordinate = None
        if not self.computer:
            while not input_valid:
                x_coordinate_guess = input("Enter the x-coordinate of the square to attack:")
                y_coordinate_guess = input("Enter the y-coordinate of the square to attach:")
                coordinate = (x_coordinate_guess, y_coordinate_guess)
                if space.are_coordinates_between_limits(coordinate, game_board.width, game_board.length):
                    input_valid = True
        else:
            coordinate = space.get_coordinates_between_limits(game_board.width, game_board.length)
        return coordinate

    @staticmethod
    def _validate_ship_placement(coordinates: list, game_board: board.BattleshipBoard) -> None:
        """ Validates that the given coordinates for ship placement on the given board are valid

        :param coordinates - a list of x and y coordinate tuples to check the validity of
        :param game_board - the board object to place the given coordinates in
        """
        for coordinate in coordinates:
            if not space.are_coordinates_between_limits(coordinate, game_board.width, game_board.length):
                raise ValueError("The location of the ship is not within the boundaries of the grid")
            if not game_board.is_square_clear(coordinate):
                raise ValueError("The location of the ship overlaps another ship")

    def _place_ship(self, ship: ships.Ship, game_board: board.BattleshipBoard):
        ship_placement_ok = False
        ship_directions = {"right", "down"}
        while not ship_placement_ok:
            try:
                if not self.computer:
                    # Receive input from human user on where and how to place the ship
                    print("Place the {0} ship of size {1}".format(ship.ship_type, ship.size))
                    direction = input("Enter either right or down for the direction the ship will face: ")
                    validation.validate_out_of_possible_options(direction, ship_directions)
                    starting_coordinate = input(
                        "Enter coordinate of left-most or top-most square to place ship in (x,y):")
                    starting_coordinate = tuple(
                        starting_coordinate.replace("(", "").replace(")", "").replace(" ", "").split(","))
                else:
                    # Pick random location to place ship if player is a computer
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
                if not self.computer:
                    print(e)
                continue

    def place_ships(self, fleet: ships.ShipFleet, game_board: board.BattleshipBoard):
        for ship_name, ship in fleet.items():
            self._place_ship(ship, game_board)
