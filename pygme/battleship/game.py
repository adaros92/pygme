from pygme.battleship import ships, player, board
from pygme.game.game import Game


class BattleshipGame(Game):

    def __init__(self,
                 config: dict, name: str = "Battleship", difficulty: str = "normal"):
        super().__init__(name, config, difficulty)
        self.players = [player.BattleshipPlayer() for _ in range(self.number_of_players)]
        # Each player will have their own board and fleet of ships to play with
        self.boards = {battleship_player.player_id: None for battleship_player in self.players}
        self.ship_fleets = {battleship_player.player_id: ships.ShipFleet(config) for battleship_player in self.players}
        # These will change depending on the current turn
        self.current_player = None
        self.other_player = None
        self.current_player_board = None
        self.other_player_board = None
        self.other_player_fleet = None

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
        self._validate_base(initialization_object)

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

    def _display_boards(self) -> None:
        # Start out with the other player's board displayed
        # Hide the locations of the enemy ships whenever the enemy's board is printed out
        ship_representations_to_hide = self.other_player_fleet.unique_ship_representations
        enemy_board_displayed = True
        self.other_player_board.print(include_reference=True, ignore_characters=ship_representations_to_hide)
        print("\nYou're looking at the other player's board.\n")
        # Provide the option to switch between boards or attack
        while True:
            player_input = input("Press b to toggle between boards or a when you're ready to make a move:")
            # Print current player's board
            if player_input == "b" and enemy_board_displayed:
                print("Your board:")
                self.current_player_board.print(include_reference=True)
                enemy_board_displayed = False
                print("\nYou're looking at your board.\n")
            # Print other player's board
            elif player_input == "b":
                self.other_player_board.print(include_reference=True, ignore_characters=ship_representations_to_hide)
                enemy_board_displayed = True
                print("\nYou're looking at the other player's board.\n")
            elif player_input == "a":
                break

    def run(self, initialization_object: dict = None) -> dict:
        self._initialize(initialization_object)
        # Keep running the game as long as no one has lost
        while not self._is_game_over():
            # Get the players involved and resolve the current turn
            self.current_player = self._next_player()
            other_players = self._other_players()
            assert (len(other_players) == 1)
            self.other_player = other_players[0]
            self.current_player_board = self.boards[self.current_player.player_id]
            # Get other player's information
            self.other_player_board = self.boards[self.other_player.player_id]
            self.other_player_fleet = self.ship_fleets[self.other_player.player_id]
            # TODO already hit logic
            # Display the boards to the current player if they're human
            if not self.current_player.computer:
                self._display_boards()
            # Attack fleet
            attack_coordinate = self.current_player.guess(self.current_player_board)
            successful_hit, ship_destroyed, already_hit = self.other_player_board.attack(
                attack_coordinate, self.other_player_fleet)
        self.print_result()
        return {}
