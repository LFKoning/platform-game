"""Module for the Player class."""

import pygame

from game.actor import Actor

class Player(Actor):

    def handle_input(self):
        """Reads input and performs associated actions."""

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.move("right")

        elif keys[pygame.K_LEFT]:
            self.move("left")

        else:
            self.stop()

        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()

    def update(self, level):
        """Updates the player."""
        self.handle_input()
        super().update(level)
