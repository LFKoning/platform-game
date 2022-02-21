"""Module for Camera classes."""

import pygame


class BaseCamera:
    """Camera base class."""

    def __init__(self, window, level):
        self._center = window / 2
        self.state = pygame.Rect(0, 0, level.width, level.height)

    def apply(self, target):
        """Moves target to the correct position."""
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.update_scroll(self.state, target.rect)

    def scroll(self, target):
        """Camera specific scrolling funtion."""
        left, top, _, _ = target.rect
        _, _, width, height = self.state.rect
        return pygame.Rect(-left + self._center.x, -top + self._center.y, width, height)


class BoundedCamera(BaseCamera):
    pass
