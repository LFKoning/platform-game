"""Module for the Actor base class."""
import pygame


class Actor:
    """Base class for all actors."""

    def __init__(self, x, y, level):
        super().__init__()

        self.level = level

        self.speed = 8
        self.direction = pygame.Vector2(0, 0)

        self.jump_speed = 16
        self.gravity = 0.8

        self.image = pygame.Surface((64, 64))
        self.image.fill("red")
        self.rect = self.image.get_rect(topleft=(x, y))

        self.on_top = None

    def __getattr__(self, attribute):
        """Re-map Rect attributes."""
        if hasattr(self.rect, attribute):
            return getattr(self.rect, attribute)
        raise AttributeError(
            f"{self.__class__.__name__} has no attribute {attribute!r}."
        )

    def move(self, direction):
        """Moves the location of the actor."""
        self.direction.x = 1 if direction == "right" else -1

    def stop(self):
        """Stops movement."""
        self.direction.x = 0

    def jump(self):
        """Makes the actor jump."""
        self.direction.y = -self.jump_speed

    def _move_horizontal(self):
        """Handle horizontal movement."""

        # No movement
        if self.direction.x == 0:
            return

        # Move the character
        self.rect.x += self.direction.x * self.speed

        # Check collisions
        collided = self._check_collision()
        if collided:
            # Bumped into something on the left
            if self.direction.x < 0:
                self.direction.x = 0
                self.rect.left = collided.right

            # Bumped into something on the right
            elif self.direction.x > 0:
                self.direction.x = 0
                self.rect.right = collided.left

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
        self.rect.y += self.direction.y

        collided = self._check_collision()
        if collided:
            # Landed on something
            if self.direction.y > 0:
                self.on_top = collided
                self.direction.y = 0
                self.rect.bottom = collided.top

            # Bumped into something above the player
            elif self.direction.y < 0:
                self.direction.y = 0
                self.rect.top = collided.bottom

    def _check_collision(self):
        """Checks for colissions."""
        for target in self.level.tiles.sprites():
            if self.rect.colliderect(target.rect):
                return target
        return None\

    def update(self):
        """Updates actor."""
        self._move_vertical()
        self._move_horizontal()
