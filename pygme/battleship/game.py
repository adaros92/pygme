import random

from pygme.battleship import ships, player
from pygme.game.game import Game


class BattleshipGame(Game):

    def __init__(self,
                 config: dict, name: str = "Battleship", number_of_players: int = 2, difficulty: str = "normal"):
        super().__init__(name, config, number_of_players, difficulty)
        self.required_inputs = {"board_width": int, "board_length": int, "difficulty": str}
        self.board = None
        self.ship_fleet = ships.ShipFleet(config)
        print(self.ship_fleet)
        self.players = [player.BattleshipPlayer() for _ in range(number_of_players)]

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
