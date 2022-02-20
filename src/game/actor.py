"""Module for the Actor base class."""
import logging

import pygame


class Actor:
    """Base class for all actors."""

    def __init__(self, name, x, y):
        super().__init__()

        self.name = name

        self.speed = 8
        self.direction = pygame.Vector2(0, 0)
        self.location = pygame.Vector2(x, y)

        self.jump_height = 16
        self.gravity = 0.8

        self.on_ground = False

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
        """Moves the actor"""

        self.faces = direction
        self.direction.x = 1 if direction == "right" else -1
        self.location.x += self.direction.x * self.speed

    def stop(self):
        """Stops movement."""
        self.direction.x = 0

    def jump(self):
        """Makes the actor jump."""
        self.direction.y = -self.jump_height

    def handle_collision(self, target):
        """Handle collision with another object."""

        # Bumped into something on the right
        # if self.direction.x > 0:
        #     overlap = self.right - target.left
        #     self.location.x -= overlap
        #     self.rect.x -= overlap
        #     self.direction.x = 0

        # # Bumped into something on the left
        # elif self.direction.x < 0:
        #     overlap = self.left - target.right
        #     self.location.x += overlap
        #     self.rect.x += overlap
        #     self.direction.x = 0

        # Landed on something
        if self.direction.y > 0:
            overlap = self.bottom - target.top
            self.location.y -= overlap
            self.rect.y -= overlap
            self.direction.y = 0
            self.on_ground = True

        # Bumped into something above the player
        elif self.direction.y < 0:
            overlap = self.top - target.bottom
            self.location.y += overlap
            self.rect.y -= overlap
            self.direction.y = 0

    def _apply_gravity(self):
        """Applies gravity to the actor."""
        if not self.on_ground:
            self.direction.y += self.gravity
            self.location.y += self.direction.y

    def update_offset(self, dx, dy):
        """Moves actor by the given offset."""
        self._offset.x += dx
        self._offset.y += dy

    def check_collision(self, targets):
        """Checks for colissions."""
        for target in targets.sprites():
            if self.rect.colliderect(target.rect):
                self.handle_collision(target)

    def update(self, level):
        """Updates actor."""

        self.rect.x = self._offset.x + self.location.x
        self.rect.y = self._offset.y + self.location.y

        self.on_ground = False
        self.check_collision(level.tiles)

        self._apply_gravity()

    def draw(self, target):
        """Draws the actor onto the game surface."""
        target.blit(self.image, (self.rect.x, self.rect.y))