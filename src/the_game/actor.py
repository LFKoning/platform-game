"""Module for the Actor base class."""
import logging

import pygame

class Actor:
    """Base class for all actors."""

    def __init__(self, name):
        self._log = logging.getLogger(f"{self.__class__.__name__}:{name}")
        self.name = name
        self.direction = pygame.Vector2(0, 0)
        self._rect = pygame.Rect()

    @property
    def l(self):
        """Returns actor left position."""
        return self._rect.x

    @property
    def r(self):
        """Returns actor right position."""
        return self.l + self.w

    @property
    def t(self):
        """Returns actor top position."""
        return self._rect.y

    @property
    def b(self):
        """Returns actor bottom position."""
        return self.t + self.h

    @property
    def w(self):
        """Returns actor width."""
        return self._rect.width

    @property
    def h(self):
        """Returns actor height."""
        return self._rect.height

    def move(self):
        """Moves the actor horizontally."""

    def jump(self):
        """Makes the actor jump."""

    def move_to(self, x, y):
        """Moves actor to the specified x and y coordinates."""

    def change_direction(self, dir_x=None, dir_y=None):
        """Changes direction for the actor."""
        if dir_x is not None:
            self.direction.x = dir_x
        if dir_y is not None:
            self.direction.y = dir_y

    def apply_gravity(self):
        """Applies gravity to the actor."""
