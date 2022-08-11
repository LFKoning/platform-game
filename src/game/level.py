"""Module for the Level class."""
import json
import logging

import pygame
from .assets import AssetMixin

from game.tiles import Tile, Tileset
from game.player import Player
from game.camera import BoundedCamera


class LevelFileError(Exception):
    """Raised when a level file contains errors."""


class Level(AssetMixin):
    """Class for loading and processing game levels."""

    required_attributes = [
        "spawn",
        "tiles",
        "tileset",
        "background",
        "gravity",
        "move_speed",
        "jump_speed",
    ]

    def __init__(self, level_path, engine):
        self.log = logging.getLogger(__name__)
        self.engine = engine

        # Create the level
        self.offset = pygame.Vector2(0, 0)
        self.level = self.load(level_path, engine.settings)
        self.tileset = Tileset(self.level["tileset"])
        self.tiles, self.bounds = self.construct(self.level["tiles"], self.tileset)

        # Create the camera
        self.camera = BoundedCamera(engine.window_size, self.bounds)

        # Add the player
        self.player = self._spawn_player()

        # Level status
        self.failed = False
        self.ended = False

    def load(self, level_path, defaults):
        """Loads a level from a JSON file."""
        self.log.debug(f"Loading level: {level_path!r}")

        # Read the file contents
        level = self.load_json(level_path)

        # Check required attributes
        for attribute in self.required_attributes:
            if not attribute in level:
                if attribute in defaults:
                    level[attribute] = defaults[attribute]
                else:
                    self.error(
                        f"Level {level_path!r} misses required attribute {attribute!r}."
                    )
        return level

    @staticmethod
    def construct(level, tileset):
        """Constructs tiles for the level."""
        tiles = pygame.sprite.Group()
        bounds = None
        for y, row in enumerate(level):

            # Store world size
            if not bounds:
                bounds = pygame.Rect(0, 0, len(row), len(level))
            else:
                if len(row) != bounds.width:
                    raise LevelFileError(
                        f"Level row {y} has {len(row)} tiles, expected {bounds.width}."
                    )

            # Build tiles for the row
            for x, code in enumerate(row):
                if code == " ":
                    continue

                tiles.add(
                    Tile(
                        x * tileset.tile_width,
                        y * tileset.tile_height,
                        tileset.find(code),
                    )
                )

        # Correct world size for tile size
        bounds.width *= tileset.tile_width
        bounds.height *= tileset.tile_height

        return tiles, bounds

    def _spawn_player(self):
        """Spawns the player into the level."""

        # Get spawn point from the level, adjust to tile size
        try:
            spawn_x, spawn_y = self.level["spawn"]
            spawn_x = int(spawn_x * self.tileset.tile_width)
            spawn_y = int(spawn_y * self.tileset.tile_height)
        except (TypeError, ValueError):
            self.error("Invalid player spawn point, use [x, y] integers.")

        return Player(spawn_x, spawn_y, self)

    def draw(self, target):
        """Updates the player, camera, and level."""

        if self.player.dead:
            self.failed = True
            self.ended = True

        self.player.update()
        self.camera.update(self.player)

        # Draw everything
        for tile in self.tiles:
            target.blit(tile.image, self.camera.apply(tile))
        target.blit(self.player.image, self.camera.apply(self.player))

    def error(self, msg):
        """Logs and handles exceptions."""
        self.log.error(msg)
        raise LevelFileError(msg)
