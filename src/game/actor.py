"""Module for the Actor base class."""
import logging

import pygame


class Actor:
    """Base class for all actors."""

    def __init__(self, name, x, y, level):
        super().__init__()

        self.name = name
        self.level = level

        self.speed = 8
        self.direction = pygame.Vector2(0, 0)
        self.location = pygame.Vector2(x, y)

        self.jump_speed = 16
        self.gravity = 0.8

        self.on_top = None

        self.image = pygame.Surface((64, 64))
        self.image.fill("red")
        self.rect = self.image.get_rect(topleft=(x, y))
        self._offset = pygame.Vector2(0, 0)

    def __getattr__(self, attribute):
        """Re-map Rect attributes."""
        if hasattr(self.rect, attribute):
            return getattr(self.rect, attribute)
        else:
            raise AttributeError(
                f"{self.__class__.__name__} has no attribute {attribute!r}."
            )

    def move(self, direction):
        """Moves the location of the actor."""
        self.faces = direction
        self.direction.x = 1 if direction == "right" else -1

    def stop(self):
        """Stops movement."""
        self.direction.x = 0

    def jump(self):
        """Makes the actor jump."""
        self.direction.y = -self.jump_speed

    def update_offset(self, dx, dy):
        """Updates the world offset."""
        self._offset.x += dx
        self._offset.y += dy

    def _move_horizontal(self):
        """Handle horizontal movement."""

        # Move the character
        self.location.x += self.direction.x * self.speed
        self.rect.x = self._offset.x + self.location.x

        # No movement
        if self.direction.x == 0:
            return

        # Check collisions
        collided = self._check_collision()
        if collided:
            # Bumped into something on the left
            if self.direction.x < 0:
                self.direction.x = 0
                overlap = self.left - collided.right
                self.location.x -= overlap
                self.rect.x -= overlap

            # Bumped into something on the right
            elif self.direction.x > 0:
                self.direction.x = 0
                overlap = self.right - collided.left
                self.location.x -= overlap
                self.rect.x -= overlap

    def _move_vertical(self):
        """Handles vertical movement."""

        # Standing on an object
        if self.on_top and self.direction.y == 0:
            # Check if still on top
            if self.left <= self.on_top.right and self.right >= self.on_top.left:
                return

        # Apply vertical movement and check collisions
        self.on_top = None
        self.direction.y += self.gravity
        self.location.y += self.direction.y
        self.rect.y = self._offset.y + self.location.y

        collided = self._check_collision()
        if collided:
            # Landed on something
            if self.direction.y > 0:
                self.on_top = collided
                self.direction.y = 0
                overlap = self.bottom - collided.top
                self.location.y -= overlap
                self.rect.y -= overlap

            # Bumped into something above the player
            elif self.direction.y < 0:
                self.direction.y = 0
                overlap = self.top - collided.bottom
                self.location.y += overlap
                self.rect.y -= overlap

    def _check_collision(self):
        """Checks for colissions."""
        for target in self.level.tiles.sprites():
            if self.rect.colliderect(target.rect):
                return target

    def update(self):
        """Updates actor."""
        self._move_vertical()
        self._move_horizontal()

    def draw(self, target):
        """Draws the actor onto the game surface."""
        target.blit(self.image, (self.rect.x, self.rect.y))
