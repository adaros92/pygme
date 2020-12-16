from pygme.battleship import ships, player, board
from pygme.game.game import Game


class BattleshipGame(Game):

    def __init__(self,
                 config: dict, name: str = "Battleship", number_of_players: int = 2, difficulty: str = "normal"):
        super().__init__(name, config, number_of_players, difficulty)
        self.required_inputs = {"board_width": int, "board_length": int, "difficulty": str}
        self.board = None
        self.ship_fleet = ships.ShipFleet(config)
        self.players = [player.BattleshipPlayer() for _ in range(number_of_players)]

    @staticmethod
    def construct_board(length: int, width: int, game_board: board.BattleshipBoard = None) -> board.BattleshipBoard:
        """ Constructs a battleship board for the game to run on

        :param length - the length of the board
        :param width - the width of the board
        :param game_board - an optional board to use instead of instantiating one
        :returns a game board to play Battleship on
        """
        if not game_board:
            game_board = board.BattleshipBoard(length, width)
        return game_board

    def _validate_initialization(self, initialization_object: dict) -> None:
        pass

    def _initialize(self, initialization_object: dict = None) -> None:
        # Assign a random player to be the human player
        self._assign_human_player()

    def _is_game_over(self) -> bool:
        pass

    def run(self, initialization_object: dict = None) -> dict:
        self._initialize(initialization_object)
        return {}
