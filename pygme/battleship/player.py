from pygme.battleship import ships
from pygme.game import player, board


class BattleshipPlayer(player.Player):

    def __init__(self, computer=False):
        super().__init__(computer=computer)

    def guess(self, game_board: board.GameBoard):
        pass

    def _place_ship(self,
                    min_coordinate: tuple, max_coordinate: tuple, ship: ships.Ship, game_board: board.GameBoard):
        pass

    def place_ships(self, fleet: ships.ShipFleet, game_board: board.GameBoard):
        pass
