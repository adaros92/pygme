import random
import time

from pygme.game.game import Game
from pygme.snake import snake, player, food
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
        self.food_collection = None
        self.current_food = []
        self.player = player.SnakePlayer()

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
        # Start monitoring player key presses
        self.player.monitor_key_presses()
        # Create a snake food collector and generator
        self.food_collection = food.FoodCollection(grid_width=board_width, grid_length=board_length)

    def _is_game_over(self) -> bool:
        """ Checks the board to see if the game is over """
        game_over = False
        end_game_coordinates = set()
        current_snake_location = self.snake.current_location
        for coordinate in current_snake_location:
            if coordinate[0] < 0 or coordinate[0] > self.board.length - 1:
                game_over = True
                break
            elif coordinate[1] < 0 or coordinate[1] > self.board.width - 1:
                game_over = True
                break
            '''
            elif coordinate in end_game_coordinates:
                game_over = True
                break
            end_game_coordinates.add(coordinate)
            '''
        return game_over

    def _get_food(self) -> None:
        difficulty_to_frequency_map = {
            "normal": 5,
            "easy": 10,
            "hard": 3
        }
        for current_food_obj in self.current_food:
            if not current_food_obj.eaten:
                return
        if random.randint(1, difficulty_to_frequency_map[self.difficulty]) == 1:
            generated_food_ok = False
            generated_foods = []
            while not generated_food_ok:
                generated_food_ok = True
                generated_foods = self.food_collection.generate()
                for generated_food in generated_foods:
                    # Don't place food in same place as Snake's head
                    if (generated_food.x_coordinate == self.snake.current_location[0][0]
                            or generated_food.y_coordinate == self.snake.current_location[0][1]):
                        # Regenerate if food is located at Snake's head
                        generated_food_ok = False
            self.current_food = generated_foods
            return
        self.current_food = []

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
            self._get_food()
            self.board.refresh(current_snake_location, representation=representation)
            for food_obj in self.current_food:
                if (current_snake_location[0][0] == food_obj.x_coordinate
                        and current_snake_location[0][1] == food_obj.y_coordinate):
                    self.snake.eat(food_obj)
                    food_obj.eaten = True
                if not food_obj.eaten:
                    self.board.refresh(
                        [(food_obj.x_coordinate, food_obj.y_coordinate)],
                        representation=food_obj.representation,
                        clear_board=False
                    )
            self.board.print()
            print("\nHit arrow keys on your keyboard to move the snake")
            # Get the current direction of the snake
            snake_direction = self.snake.current_direction
            # Get directional input from the user about where to go
            for key in ["left", "right", "up", "down"]:
                if self.player.key_pressed_map[key]:
                    snake_direction = key
                    break
            self.snake.move(snake_direction)
            game_over = self._is_game_over()
            if game_over:
                print("Game over! Hit <Enter> to exit.")
                self.player.finished_game = True
                self.player.wait_for_player_to_finish()
                break
            else:
                time.sleep(.25)
        return {}
