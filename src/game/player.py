"""Module for the Player class."""
import logging
from pathlib import Path

import pygame

from game.actor import Actor
from game.assets import AssetMixin


class Player(Actor, AssetMixin):
    """Class for the player.

    Parameters
    ----------
    x : int
        Horizontal spawn location for the player.
    y : int
        vertical spawn location for the player.
    level: game.level.Level
        Reference to the current level.
    """

    def __init__(self, x: int, y: int, level: "Level") -> None:
        self.log = logging.getLogger(self.__class__.__name__)

        animation_path = Path.cwd() / "assets/gfx/player"
        super().__init__(x, y, 64, 64, animation_path, level)

    def handle_input(self) -> None:
        """Reads input and performs associated actions."""

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.move("right")

        elif keys[pygame.K_LEFT]:
            self.move("left")

        else:
            self.stop()

        if keys[pygame.K_SPACE] and self.on_top:
            self.jump()
