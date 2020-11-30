from pygme.utils.display import clear_console
from pygme.utils.validation import validate_grid_index


class GameBoard(object):
    """ Represents a base board to play a game on which may be extended by more specific types of boards

    Constructor arguments:

    :param length - the length of the board to create
    :param width - the width of the board to create
    """
    def __init__(self, length: int, width: int) -> None:
        assert length > 0 and width > 0
        self.length = length
        self.width = width
        self.board = []
        self._create_board()

    def _create_board(self) -> None:
        """ Creates an empty 2D list with the given board dimensions"""
        for i in range(self.length):
            self.board.append([None for _ in range(self.width)])

    def print(self, empty_square: str = '_') -> None:
        """ Prints out the board to stdout

        :param empty_square - how to represent empty squares on the board
        """
        # Clear the terminal
        clear_console()
        # Print the current board
        for i in range(self.width):
            print(' '.join([empty_square if not self.board[square][i]
                            else self.board[square][i] for square in range(self.length)]))

    def clear(self, empty_square: any = '_') -> None:
        """ Clears the current board by replacing every square with the given empty square character

        :param empty_square - how to represent empty squares when showing the board to the user or passing downstream
        """
        for i in range(self.width):
            for j in range(self.length):
                self.board[j][i] = empty_square

    def refresh(self,
                coordinates: list, representation: str, empty_square: str = '_', clear_board: bool = True) -> None:
        """ Refreshes the board by adding the given representation character to the given coordinates

        Example: representation = '*' at coordinates [(0, 1), (2, 1)] on a 3x3 board will result in the following:
        _ _ _
        * _ *
        _ _ _

        :param coordinates - a list of coordinate tuples to update
        :param representation - the character to be placed in the given coordinates
        :param empty_square - the character to represent empty squares
        :param clear_board - whether to first clear the current board before placing the new characters or not
        """
        # Clear the current board first if the provided argument is true
        if clear_board:
            self.clear(empty_square)
        for coordinate_tuple in coordinates:
            x_coordinate, y_coordinate = coordinate_tuple[0], coordinate_tuple[1]
            # Only refresh the board with the coordinate if the coordinate is valid
            if validate_grid_index(self.length, self.width, x_coordinate, y_coordinate):
                # Refresh the board
                self.board[x_coordinate][y_coordinate] = representation

    def __repr__(self):
        return "GameBoard ({0} by {1})".format(self.length, self.width)

    def __str__(self):
        return self.__repr__()
