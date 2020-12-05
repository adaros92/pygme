from pygme.game.player import Player


class BattleshipPlayer(Player):

    def __init__(self, computer=False):
        super().__init__(computer=computer)

    def guess(self, board):
        pass
