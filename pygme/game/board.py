

class GameBoard(object):
    def __init__(self, length: int, width: int) -> None:
        """ Creates a game board given the length and width in number of squares """
        assert length > 0 and width > 0
        self.length = length
        self.width = width
        self.board = []
        self._create_board()

    def _create_board(self) -> None:
        """ Creates a 2D list for the game board """
        for i in range(self.length):
            self.board.append([None for _ in range(self.width)])

    def print(self, empty_square: str = '0', occupied_square: str = '*') -> None:
        """ Prints out the board to stdout

        :param empty_square - how to represent empty squares on the board
        :param occupied_square - how to represent occupied squares on the board
        """
        # Clear the terminal
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
        # Print the current board
        for i in range(self.width):
            print(' '.join([empty_square if not self.board[square][i]
                            else occupied_square for square in range(self.length)]))

    def __repr__(self):
        return "GameBoard ({0} by {1})".format(self.length, self.width)

    def __str__(self):
        return self.__repr__()
