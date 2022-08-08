"""Game engine module."""
import logging

import pygame

from game.level import Level


class EngineError(Exception):
    """Raised when the game engine encounters an error."""


class GameEngine:
    """Game engine class, handles screen, actors and events.

    Parameters
    ----------
    windows_size : tuple of int
        Tuple of window width and height.
    fps : int
        Frames per second.
    """

    def __init__(self, settings):
        self.log = logging.getLogger(self.__class__.__name__)

        self.settings = settings
        self.name = settings.get("game_name", "My Game")
        self.log.info(f"Starting game: {self.name!r}")

        self.log.debug("Initializing pygame.")

        # Get and check game settings
        try:
            width = int(settings.get("window_width", 1000))
        except ValueError:
            self.error("Window width should be an integer.")
        try:
            height = int(settings.get("window_height", 800))
        except ValueError:
            self.error("Window height should be an integer.")
        try:
            self.fps = int(settings.get("fps", 60))
        except ValueError:
            self.error("FPS should be an integer.")
        self._bg_color = settings.get("background", "black")
        try:
            self._bg_color = pygame.Color(self._bg_color)
        except ValueError:
            self.error(f"Invalid background color: {self._bg_color!r}.")

        # Create the game window
        self.log.debug(f"Creating window: {width} x {height}.")
        self.window_size = pygame.Vector2(width, height)
        self.window = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption(self.name)
        self._clock = pygame.time.Clock()

        # Load the first level
        if not settings.get("levels"):
            self.error("No levels supplied, nothing left to play.")
        self._level_nr = -1
        self.level = None
        self._next_level()

    def _next_level(self):
        """Loads the next game level."""
        levels = self.settings.get("levels")
        if len(levels) > self._level_nr + 1:
            self._level_nr += 1
            self.level = Level(levels[self._level_nr], self)
        else:
            self.end_game()

    def end_game(self):
        """Finishes the game"""
        # TODO: End game screen / credits / etc.
        self.log.info("Ending the game.")
        pygame.quit()

    def run(self):
        """Start the engine."""
        pygame.init()
        running = True
        while running:
            self._clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.log.info(f"Ending game: {self.name!r}")
                    running = False
                    break

            running = self.draw()

    def draw(self):
        """Redraws the screen."""
        if not self.level.ended:
            self.window.fill(self._bg_color)
            self.level.draw(self.window)
            pygame.display.update()
            return True

        if self.level.failed:
            self.log.info("Oh noes, you failed the level...")
        else:
            self.log.info("Hurrah you finished the level...")
        return False

    def error(self, msg):
        """Logs and handles exceptions."""
        self.log.error(msg)
        raise EngineError(msg)
