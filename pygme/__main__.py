import argparse

from pygme.snake import game

SUPPORTED_GAMES = {"snake": game.SnakeGame, "adventure": None, "tetris": None}


def parse_args():
    """ Parse arguments passed in via the CLI
    :returns a parsed argument object from argparse
    """
    parser = argparse.ArgumentParser()
    # Accept the operation to perform
    parser.add_argument('game', choices=[game_name for game_name in SUPPORTED_GAMES], help="choose the game to play")
    return parser.parse_args()


def main():
    # Get arguments from CLI
    args = parse_args()
    # Instantiate and run corresponding game class
    game_object = SUPPORTED_GAMES[args.game]()
    if not game_object:
        raise RuntimeError("Game is unavailable. Check back later!")
    game_object.run()


if __name__ == "__main__":
    main()
