"""Game engine module."""
import logging

import pygame

from settings import SETTINGS


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

    def __init__(self):
        self._log = logging.getLogger(__name__)

        self.name = SETTINGS.get("game_name", "My Game")
        self._log.info(f"Starting game: {self.name!r}")

        self._log.debug("Initializing pygame.")
        pygame.init()

        try:
            width = int(SETTINGS.get("window_width", 1000))
        except ValueError:
            raise EngineError("Window width should be an integer.")
        try:
            height = int(SETTINGS.get("window_height", 800))
        except ValueError:
            raise EngineError("Window height should be an integer.")

        # Create the game window
        self._log.debug(f"Creating window: {width} x {height}.")
        self._window = pygame.display.set_mode((width, height))
        pygame.display.set_caption(self.name)
        self._clock = pygame.time.Clock()

        try:
            self.fps = int(SETTINGS.get("fps", 60))
        except ValueError:
            raise EngineError("FPS should be an integer.")

        bg_color = SETTINGS.get("background", "black")
        try:
            self._bg_color = pygame.Color(bg_color)
        except ValueError:
            raise EngineError(f"Invalid background color: {bg_color!r}.")

        running = True
        while running:
            self._clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._log.info(f"Ending game: {self.name!r}")
                    running = False
                    break

            self._draw()

    def _draw(self):
        """Redraws the screen."""

        self._window.fill(self._bg_color)
        pygame.display.update()