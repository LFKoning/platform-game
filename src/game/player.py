"""Module for the Player class."""
from pathlib import Path
from itertools import cycle

import pygame

from game.actor import Actor
from game.assets import AssetMixin


class Player(Actor, AssetMixin):
    """Class for the player."""

    def __init__(self, x, y, level):
        super().__init__(x, y, 33, 33, level)

    def handle_input(self):
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

    def load_animations(self):
        """Loads player animations"""

        animations = {}
        for animation in "idle", "jump", "run":
            anim_path = Path.cwd() / "assets/gfx/player" / animation
            images = anim_path.glob("*.png")

            images = cycle([self.load_image(i).convert_alpha() for i in images])
            animations[animation] = images

        return animations
