from abc import ABC, abstractmethod

from pygme.game.board import GameBoard


class Game(ABC):

    DIFFICULTY_TYPES = {"easy", "normal", "hard"}

    def __init__(self, name: str, number_of_players: int = 1, levels: int = 10, difficulty: str = "normal") -> None:
        self.name = name
        self.number_of_players = number_of_players
        self.levels = levels
        self.difficulty = difficulty

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
    def run(self, initialization_object: dict) -> dict:
        pass
