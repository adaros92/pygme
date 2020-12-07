import argparse
import json
import os
import pkg_resources

from pygme.snake.game import SnakeGame
from pygme.battleship.game import BattleshipGame

SUPPORTED_GAMES = {"snake": SnakeGame, "adventure": None, "tetris": None, "battleship": BattleshipGame}


def _load_config():
    directory_path = pkg_resources.resource_filename('pygme', 'data/')
    full_path = os.path.join(directory_path, "config.json")
    with open(full_path, "r") as f:
        config = json.load(f)
    return config


def _validate_config(config):
    for game_name in SUPPORTED_GAMES:
        if game_name not in config:
            raise ValueError("The provided config in pygme/data/config.json must have settings for {0}".format(
                game_name))


def _parse_args():
    """ Parse arguments passed in via the CLI
    :returns a parsed argument object from argparse
    """
    parser = argparse.ArgumentParser()
    # Accept the operation to perform
    parser.add_argument('game', choices=[game_name for game_name in SUPPORTED_GAMES], help="choose the game to play")
    return parser.parse_args()


def main():
    # Load configuration and validate it
    config = _load_config()
    _validate_config(config)
    # Get arguments from CLI
    args = _parse_args()
    # Instantiate and run corresponding game class with provided config
    game_class = SUPPORTED_GAMES[args.game]
    if not game_class:
        raise RuntimeError("Game is unavailable. Check back later!")
    game_object = game_class(config=config[args.game])
    game_object.run()


if __name__ == "__main__":
    main()
