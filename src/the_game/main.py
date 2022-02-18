"""Main game module."""
import logging

from engine import GameEngine

def run():
    """Sets up and starts the game."""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    engine = GameEngine()

if __name__ == "__main__":
    run()