"""Module for the Actor base class."""
import logging

import pygame


class Actor:
    """Base class for all actors."""

    def __init__(self, x, y, w, h, level):
        self.log = logging.getLogger(self.__class__.__name__)
        self.level = level

        # Define positional info
        self.rect = pygame.Rect(x, y, w, h)
        self.direction = pygame.Vector2(0, 0)

        # Define speeds
        self.speed = 8
        self.jump_speed = 16
        self.gravity = 0.8

        self.last_tick = -1
        self.animations = self.load_animations()

        self.dead = False
        self.on_top = None

    def load_animations(self):
        """Should be overwritten by child classes."""
        return {}

    def move(self, direction):
        """Moves the location of the actor."""
        self.direction.x = 1 if direction == "right" else -1

    def stop(self):
        """Stops movement."""
        self.direction.x = 0

    def jump(self):
        """Makes the actor jump."""
        self.direction.y = -self.jump_speed

    def move_horizontal(self):
        """Handle horizontal movement."""

        # No movement
        if self.direction.x == 0:
            return

        # Check world bounds
        if self.rect.x == 0 and self.direction.x < 0:
            return
        if self.rect.right == self.level.bounds.width and self.direction.x > 0:
            return

        # Move the character
        self.rect.x += self.direction.x * self.speed

        # Check collisions
        collided = self.check_collision()
        if collided:
            # Bumped into something on the left
            if self.direction.x < 0:
                self.direction.x = 0
                self.rect.left = collided.right

            # Bumped into something on the right
            elif self.direction.x > 0:
                self.direction.x = 0
                self.rect.right = collided.left

    def move_vertical(self):
        """Handles vertical movement."""

        # Check world bounds
        if self.rect.top >= self.level.bounds.height:
            self.dead = True

        # Standing on an object
        if self.on_top and self.direction.y == 0:
            # Check if still on top
            if self.left <= self.on_top.right and self.right >= self.on_top.left:
                return

        # Apply vertical movement and check collisions
        self.on_top = None
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

        collided = self.check_collision()
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

    def check_collision(self):
        """Checks for colissions."""
        for target in self.level.tiles.sprites():
            if self.rect.colliderect(target.rect):
                return target
        return None

    def update(self):
        """Updates the actor."""

        # Actor is controlled by a player
        if hasattr(self, "handle_input"):
            self.handle_input()

        # Handle actor movement
        self.move_vertical()
        self.move_horizontal()

        self.play_animation()

    def play_animation(self):
        """Plays actor's animations."""

        flip_horizontal = False
        if self.direction.x > 0:
            animation = "run"
        elif self.direction.x < 0:
            animation = "run"
            flip_horizontal = True
        else:
            animation = "idle"

        tick = pygame.time.get_ticks()
        if animation in self.animations:
            if self.last_tick == -1 or tick - self.last_tick > 100:
                self.image = next(self.animations[animation])
                if flip_horizontal:
                    self.image = pygame.transform.flip(self.image, True, False)
                self.last_tick = tick

    def __getattr__(self, attribute):
        """Re-map Rect attributes."""
        if hasattr(self.rect, attribute):
            return getattr(self.rect, attribute)
        raise AttributeError(
            f"{self.__class__.__name__} has no attribute {attribute!r}."
        )
