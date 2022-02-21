"""Module for Camera classes."""

import pygame


class BasicCamera:
    """Basic camera class."""

    def __init__(self, window_size, level_bounds):
        self.window = window_size
        self.center = window_size / 2
        self.bounds = level_bounds
        self.state = pygame.Rect(0, 0, level_bounds.width, level_bounds.height)

    def apply(self, target):
        """Moves target to the correct position."""
        return target.rect.move(self.state.topleft)

    def update(self, target):
        """Updates state to the location of the target."""
        self.state = self.scroll(target)

    def scroll(self, target):
        """Camera specific scrolling funtion."""
        left, top = target.rect.left, target.rect.top
        return pygame.Rect(
            -left + self.center.x,
            -top + self.center.y,
            self.bounds.width,
            self.bounds.height,
        )


class BoundedCamera(BasicCamera):
    """Camera restricted by level bounds."""

    def scroll(self, target):
        """Scrolls until a world boundary is hit."""
        # Scroll as usual
        new_state = super().scroll(target)

        # Apply restrictions
        new_state.x = max(-(self.bounds.width - self.window.x), min(0, new_state.x))
        new_state.y = max(-(self.bounds.height - self.window.y), min(0, new_state.y))

        return new_state
