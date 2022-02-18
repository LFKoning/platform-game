"""Module for the Level class."""
import json
import logging

import pygame

from game.tiles import Tile, Tileset


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

    def __init__(self, level_path, defaults):
        self._log = logging.getLogger(__name__)
        self._defaults = defaults

        self._level = self._load(level_path)

        try:
            self.spawn = pygame.Vector2(self._level["spawn"])
        except ValueError:
            self._error(f"Level {level_path!r} has an invalid spawn point.")

        tileset = Tileset(self._level["tileset"])
        self._tiles = self.construct(self._level["tiles"], tileset)

    def _load(self, level_path):
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
                if attribute in self._defaults:
                    level[attribute] = self._defaults[attribute]
                else:
                    self._error(
                        f"Level {level_path!r} misses required attribute {attribute!r}."
                    )

        return level

    def construct(self, level, tileset):
        """Constructs tiles for the level."""
        tiles = pygame.sprite.Group()
        for y, row in enumerate(level):
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

        return tiles

    def draw_tiles(self, target):
        """Draws tiles on the target surface."""
        self._tiles.draw(target)

    def _error(self, msg):
        """Logs and handles exceptions."""
        self._log.error(msg)
        raise LevelFileError(msg)
