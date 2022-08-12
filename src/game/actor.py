"""Module for the Actor base class."""
import logging

from typing import Any
from pathlib import Path
from itertools import cycle

import pygame


class Actor:
    """Base class for all actors.

    Parameters
    ----------
    x : int
        Horizontal spawn location for the actor.
        Measured as pixels from top left corner of the level.
    y : int
        Vertical spawn location for the player
        Measured as pixels from top left corner of the level.
    width : int
        Width of the actor in pixels.
    height : int
        Height of the actor in pixels.
    animation_path : pathlib.Path
        Path to the animations base folder.
    level : game.level.Level
        Reference to the current level.
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        animation_path: Path,
        level: "Level",
    ) -> None:
        self.log = logging.getLogger(self.__class__.__name__)
        self.level = level

        # Define positional info
        self.width = width
        self.height = 64
        self.rect = pygame.Rect(x, y, width, height)
        self.direction = pygame.Vector2(0, 0)

        # Define speeds
        self.speed = 8
        self.jump_speed = 16
        self.gravity = 0.8

        self.last_animation = None
        self.last_tick = -1
        self.animations = self.load_animations(animation_path)

        self.dead = False
        self.on_top = None

    def load_animations(self, base_path: Path) -> dict:
        """Loads player animations.

        Parameters
        ----------
        base_path : Path
            Path to the actors animations folder.

        Returns
        -------
        dict
            Dict mapping animations to cycles of images.
        """

        animations = {}
        for animation in "fall", "idle", "jump", "run":
            anim_path = base_path / animation
            images = anim_path.glob("*.png")

            images = cycle(
                [
                    pygame.transform.scale(
                        self.load_image(i).convert_alpha(), (self.width, self.height)
                    )
                    for i in images
                ]
            )
            animations[animation] = images

        return animations

    def move(self, direction: str) -> None:
        """Move the actor in the provided direction.

        Parameters
        ----------
        direction : {"left", "right"}
            Direction to move the actor in.
        """
        self.direction.x = 1 if direction == "right" else -1

    def stop(self) -> None:
        """Stop actor movement."""
        self.direction.x = 0

    def jump(self) -> None:
        """Make the actor jump."""
        self.direction.y = -self.jump_speed

    def move_horizontal(self) -> None:
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

    def move_vertical(self) -> None:
        """Handle vertical movement."""

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

    def check_collision(self) -> None:
        """Check for colissions between the actor and tiles."""
        for target in self.level.tiles.sprites():
            if self.rect.colliderect(target.rect):
                return target
        return None

    def update(self) -> None:
        """Updates the actor."""

        # Actor is controlled by a player
        if hasattr(self, "handle_input"):
            self.handle_input()

        # Handle actor movement
        self.move_vertical()
        self.move_horizontal()

        self.play_animation()

    def play_animation(self) -> None:
        """Play actor animations."""

        if self.direction.y < 0:
            animation = "jump"
        elif self.direction.y > 0:
            animation = "fall"
        elif self.direction.x != 0:
            animation = "run"
        else:
            animation = "idle"

        flip_horizontal = True if self.direction.x < 0 else False

        tick = pygame.time.get_ticks()
        if animation in self.animations:
            if self.last_animation != animation or tick - self.last_tick > 100:
                self.image = next(self.animations[animation])
                if flip_horizontal:
                    self.image = pygame.transform.flip(self.image, True, False)

                self.last_animation = animation
                self.last_tick = tick

    def __getattr__(self, attribute: str) -> Any:
        """Map unknown attributes to actor Rect.

        Parameters
        ----------
        attribute : str
            Attribute to retrieve.

        Returns
        -------
        Any
            The attribute's value.

        Raises
        ------
        AttributeError
            Raised when actor Rect does not have the attribute.
        """
        if hasattr(self.rect, attribute):
            return getattr(self.rect, attribute)
        raise AttributeError(
            f"{self.__class__.__name__} has no attribute {attribute!r}."
        )
