from abc import ABC, abstractmethod
import random

from pygme.game.board import GameBoard
from pygme.game.player import Player


class Game(ABC):

    DIFFICULTY_TYPES = {"easy", "normal", "hard"}

    def __init__(self, name: str, number_of_players: int = 1, levels: int = 10, difficulty: str = "normal") -> None:
        self.name = name
        self.number_of_players = number_of_players
        self.levels = levels
        self.difficulty = difficulty
        self.players = []
        self.player_turn = 0

    def _assign_human_player(self):
        """ Makes a random player in the list of players the human player """
        # Get random index based on length of player list
        random_index = random.randint(0, len(self.players) - 1)
        # Assign a random player in that list to be the human player
        # This player will require input from the current user while the others will play on their own
        self.players[random_index].computer = False

    def _next_player(self) -> Player:
        """ Retrieves the next player in line to play

        :returns a player object retrieved from the list of current players
        """
        player_count = len(self.players)
        if player_count == 0:
            raise RuntimeError("There are no active players in the {0} game".format(self.name))
        # If it's the last player then get the first player in the list
        if self.player_turn == len(self.players) - 1:
            self.player_turn = 0
        # Otherwise get the next player in the list
        else:
            self.player_turn += 1
        return self.players[self.player_turn]

    @staticmethod
    def construct_board(length, width, board: GameBoard = None) -> GameBoard:
        if not board:
            board = GameBoard(length, width)
        return board

    @abstractmethod
    def _validate_initialization(self, initialization_object: dict) -> None:
        pass

    @abstractmethod
    def _initialize(self, initialization_object: dict = None) -> None:
        pass

    @abstractmethod
    def _is_game_over(self) -> bool:
        pass

    @abstractmethod
    def run(self, initialization_object: dict) -> dict:
        pass
