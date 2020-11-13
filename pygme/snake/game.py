import random
import time

from pygme.game.game import Game
from pygme.snake import snake
from pygme.utils.display import clear_console
from pygme.utils.validation import validate_user_input


class SnakeGame(Game):
    """ Defines the main Snake game loop and initialization functionality """

    def __init__(self,
                 name: str = "Snake", number_of_players: int = 1, levels: int = 10, difficulty: str = "normal") -> None:
        super().__init__(name, number_of_players, levels, difficulty)
        self.required_inputs = {"board_width": int, "board_length": int, "difficulty": str}
        self.board = None
        self.snake = None

    def _validate_initialization(self, initialization_object: dict) -> None:
        """ Ensures that the given initialization_object containing parameters to run the Snake game has complete
        and valid parameters

        :param initialization_object - a dictionary containing game parameter names and their values for operation
        """
        # Validate completeness of inputs
        for required_input in self.required_inputs:
            if required_input not in initialization_object:
                raise RuntimeError("{0} is a required input to begin a Snake game".format(required_input))
        # Validate correct board dimensions
        board_width = initialization_object["board_width"]
        board_length = initialization_object["board_length"]
        difficulty = initialization_object["difficulty"]
        required_width = 10
        required_length = 10
        if initialization_object["board_width"] < required_width \
                or initialization_object["board_length"] < required_length:
            raise ValueError("The Snake board must be at least {0}x{1}".format(required_length, required_width))
        if board_width != board_length:
            raise ValueError("The Snake board must be a square where width == length")
        if difficulty not in self.DIFFICULTY_TYPES:
            raise ValueError("The game difficulty must be one of {0}".format(self.DIFFICULTY_TYPES))

    def _initialize(self, initialization_object: dict = None) -> None:
        """ Initializes a game of Snake from the given object of game parameters or user input if one is not provided

        :param initialization_object - a dictionary containing game parameter names and their values for operation
        """
        # Get input from the user if no initialization_object is provided
        if not initialization_object:
            initialization_object = {}
            pre_prompt = ""
            while True:
                clear_console()
                try:
                    print("{0}Provide your inputs to begin your game of Snake. Difficulty levels: easy, normal, hard\n"
                          .format(pre_prompt))
                    for required_input, input_type in self.required_inputs.items():
                        input_val = input("Enter a value for {0}: ".format(required_input))
                        initialization_object[required_input] = validate_user_input(
                            required_input, input_val, input_type)
                    self._validate_initialization(initialization_object)
                    break
                except Exception as e:
                    pre_prompt = str(e) + "\n\n"
                    pass
        # Validate the input passed through the method arguments
        else:
            self._validate_initialization(initialization_object)
        # Create the board
        board_width = initialization_object["board_width"]
        board_length = initialization_object["board_length"]
        difficulty = initialization_object["difficulty"]
        self.board = self.construct_board(board_length, board_width)
        # Pick a random point to place the snake on and a starting snake length based on chosen difficulty
        starting_x_coordinate = random.randint(2, board_length-3)
        starting_y_coordinate = random.randint(2, board_width-3)
        starting_length = {"easy": 2, "normal": 4, "hard": 8}[difficulty]
        self.snake = snake.Snake(
            x_coordinate=starting_x_coordinate, y_coordinate=starting_y_coordinate, starting_length=starting_length)

    def run(self, initialization_object: dict = None) -> dict:
        """ Game loop that accepts player events to move the snake around the board and keeps the state of the game
        until the game finishes

        :param initialization_object - a dictionary containing game parameter names and their values for operation
        :returns a dictionary containing various metrics and their values about the game that was played
        """
        self._initialize(initialization_object)
        representation = str(self.snake)[0]
        while True:
            current_snake_location = self.snake.current_location
            self.board.refresh(current_snake_location, representation=representation)
            self.board.print()
            self.snake.move("up")
            time.sleep(1)
        return {}