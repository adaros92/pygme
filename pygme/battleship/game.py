from pygme.battleship import ships, player, board
from pygme.game.game import Game


class BattleshipGame(Game):

    def __init__(self,
                 config: dict, name: str = "Battleship", difficulty: str = "normal"):
        number_of_players = 2
        super().__init__(name, config, number_of_players, difficulty)
        self.players = [player.BattleshipPlayer() for _ in range(number_of_players)]
        # Each player will have their own board and fleet of ships to play with
        self.boards = {battleship_player.player_id: None for battleship_player in self.players}
        self.ship_fleets = {battleship_player.player_id: ships.ShipFleet(config) for battleship_player in self.players}

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
        # Get input from the user if no initialization_object is provided
        initialization_object = self._get_user_input(initialization_object)
        board_width = initialization_object["board_width"]
        board_length = initialization_object["board_length"]
        difficulty = initialization_object["difficulty"]
        self.boards = {player_id: self.construct_board(board_length, board_width)
                       for player_id, _ in self.boards.items()}
        for player_obj in self.players:
            player_id = player_obj.player_id
            player_obj.place_ships(
                fleet=self.ship_fleets[player_id],
                game_board=self.boards[player_id]
            )

    def _is_game_over(self) -> bool:
        """ Checks whether the game has finished and determines a winner

        :returns True if the game has finished, False otherwise
        """
        for player_in_game in self.players:
            if self.ship_fleets[player_in_game.player_id].is_destroyed():
                player_in_game.winner = False
                return True
        return False

    def run(self, initialization_object: dict = None) -> dict:
        self._initialize(initialization_object)
        # Keep running the game as long as no one has lost
        while not self._is_game_over():
            # Get the next player in line to play
            battleship_player = self._next_player()
            other_players = self._other_players()
            assert(len(other_players) == 1)
            other_player = other_players[0]
            game_board = self.boards[battleship_player.player_id]
            game_board.print(include_reference=True)
            # Ask the player to guess coordinates to attack
            attack_coordinate = battleship_player.guess(game_board)
            # Attack the player's fleet on their board
            player_board = self.boards[other_player.player_id]
            player_fleet = self.ship_fleets[other_player.player_id]
            successful_hit, ship_destroyed, already_hit = player_board.attack(attack_coordinate, player_fleet)
        self.print_result()
        return {}
