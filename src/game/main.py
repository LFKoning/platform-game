"""Main game module."""
import logging

from game.settings import SETTINGS
from game.engine import GameEngine


def run() -> None:
    """Sets up and starts the game."""
    logging.basicConfig(level=logging.DEBUG)
    engine = GameEngine(SETTINGS)
    engine.run()


if __name__ == "__main__":
    run()
