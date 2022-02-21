"""Module for the Level class."""
import json
import logging

import pygame

from game.tiles import Tile, Tileset
from game.player import Player
from game.camera import BoundedCamera


class LevelFileError(Exception):
    """Raised when a level file contains errors."""


class Level:
    """Class for loading and processing game levels."""

    _required = [
        "spawn",
        "tiles",
        "tileset",
        "background",
        "gravity",
        "move_speed",
        "jump_speed",
    ]

    def __init__(self, level_path, engine):
        self._log = logging.getLogger(__name__)
        self._offset = pygame.Vector2(0, 0)

        # Create the level
        self._level = self._load(level_path, engine.settings)
        self._tileset = Tileset(self._level["tileset"])
        self.tiles, self.bounds = self._construct(self._level["tiles"], self._tileset)

        # Create the camera
        self._camera = BoundedCamera(engine.window_size, self.bounds)

        # Add the player
        self.player = self._spawn_player()

    def _load(self, level_path, defaults):
        """Loads a level from a JSON file."""
        self._log.debug(f"Loading level: {level_path!r}")

        # Read the file contents
        try:
            with open(level_path, "r", encoding="utf-8") as level_file:
                level = json.load(level_file)

        except FileNotFoundError:
            self._error(f"Cannot find level file: {level_path!r}.")
        except json.decoder.JSONDecodeError:
            self._error(f"Level {level_path!r} is not valid JSON.")

        # Check required attributes
        for attribute in self._required:
            if not attribute in level:
                if attribute in defaults:
                    level[attribute] = defaults[attribute]
                else:
                    self._error(
                        f"Level {level_path!r} misses required attribute {attribute!r}."
                    )

        return level

    @staticmethod
    def _construct(level, tileset):
        """Constructs tiles for the level."""
        tiles = pygame.sprite.Group()
        bounds = None
        for y, row in enumerate(level):
            if not bounds:
                bounds = pygame.Rect(0, 0, len(row), len(level))
            else:
                if len(row) != bounds.width:
                    raise LevelFileError(
                        f"Level row {y} has {len(row)} tiles, expected {bounds.width}."
                    )

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

        # Adjust bounds to tile size
        bounds.width *= tileset.tile_width
        bounds.height *= tileset.tile_height

        return tiles, bounds

    def _spawn_player(self):
        """Spawns the player into the level."""

        # Get spawn point from the level, adjust to tile size
        try:
            spawn_x, spawn_y = self._level["spawn"]
            spawn_x = int(spawn_x * self._tileset.tile_width)
            spawn_y = int(spawn_y * self._tileset.tile_height)
        except (TypeError, ValueError):
            self._error("Invalid player spawn point, use [x, y] integers.")

        return Player(spawn_x, spawn_y, self)

    def draw(self, target):
        """Draws tiles on the target surface."""

        self.player.update()
        self._camera.update(self.player)

        # Draw everything
        for tile in self.tiles:
            target.blit(tile.image, self._camera.apply(tile))
        target.blit(self.player.image, self._camera.apply(self.player))

    def _error(self, msg):
        """Logs and handles exceptions."""
        self._log.error(msg)
        raise LevelFileError(msg)
