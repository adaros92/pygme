import uuid

from abc import ABC, abstractmethod


class Player(ABC):

    def __init__(self, player_id: uuid.UUID = uuid.uuid1()):
        self.player_id = str(player_id)
        self.finished_game = False

    @abstractmethod
    def _detect_key_pressed(self) -> None:
        pass

    @abstractmethod
    def monitor_key_presses(self, key: str = None, how: str = "thread") -> None:
        pass
