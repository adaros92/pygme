from pygme.battleship import ships, board
from pygme.game import player
from pygme.utils import space


class BattleshipPlayer(player.Player):

    def __init__(self, computer=True):
        super().__init__(computer=computer)

    def _get_coordinate_from_input(self) -> tuple:
        """ Accepts user attack coordinate input

        :returns a tuple containing the X and Y coordinates received as user input
        """
        x_coordinate_guess = int(input("Enter the x-coordinate of the square to attack:"))
        y_coordinate_guess = int(input("Enter the y-coordinate of the square to attach:"))
        return x_coordinate_guess, y_coordinate_guess

    def _human_guess(self, game_board: board.BattleshipBoard) -> tuple:
        """ Accept an attack guess from a human player as raw input

        :param game_board - the board where ships to attack are currently located
        :returns a tuple containing the X and Y coordinates of the square to attack
        """
        input_valid = False
        coordinate = None
        while not input_valid:
            try:
                coordinate = self._get_coordinate_from_input()
            except ValueError:
                print("Individual coordinate components must be single integers")
                continue
            if space.are_coordinates_between_limits(coordinate, game_board.width, game_board.length):
                input_valid = True
        return coordinate

    def _computer_guess(self, game_board: board.BattleshipBoard) -> tuple:
        """ Run computer attack guessing algorithm

        :param game_board - the board where ships to attack are currently located
        :returns a tuple containing the X and Y coordinates of the square to attack
        """
        # TODO Implement a smart guessing algorithm
        return space.get_coordinates_between_limits(game_board.width, game_board.length)

    def guess(self, game_board: board.BattleshipBoard) -> tuple:
        """ Each player will guess the other's ships' locations and attack them one at a time

        :param game_board - the board where ships are currently located
        :returns a tuple containing the X and Y coordinates of the square to attack
        """
        # Accept input from player if they're not the computer
        if not self.computer:
            coordinate = self._human_guess(game_board)
        # Follow guessing algorithm if computer
        else:
            coordinate = self._computer_guess(game_board)
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
                # Choose a random location and starting direction
                board_width, board_length = game_board.width, game_board.length
                starting_coordinate = space.get_coordinates_between_limits(board_width, board_length)
                direction = space.get_random_directions(list(ship_directions), 1)[0]
                # Retrieve the coordinates based random starting location of ships
                coordinates = space.get_contiguous_coordinates(starting_coordinate, direction, ship.size)
                # Raise exception if any of the ships go beyond the board or if they overlap others
                self._validate_ship_placement(coordinates, game_board)
                # Let ship object know that it is placed on a grid
                ship.place_ship(coordinates)
                ship_placement_ok = True
                # Update the board with the new ship
                game_board.place_ship(ship)
            except ValueError as e:
                continue

    def place_ships(self, fleet: ships.ShipFleet, game_board: board.BattleshipBoard) -> None:
        """ Places each ship in the given fleet on the given board

        :param fleet - the fleet containing ships to be placed on the board
        :param game_board - the board to place the ships on
        """
        for ship_name, ship in fleet.items():
            self._place_ship(ship, game_board)
