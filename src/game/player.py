"""Module for the Player class."""

import pygame

from game.actor import Actor


class Player(Actor):
    """Class for the player."""

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

    def update(self):
        """Updates the player."""
        self.handle_input()
        super().update()
