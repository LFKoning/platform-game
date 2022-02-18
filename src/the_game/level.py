"""Module for the Level class."""
import json
import logging


class LevelFileError(Exception):
    """Raised when a level file contains errors."""


class Level:
    """Class for loading and processing game levels."""

    _required = [
        "tiles",
        "backdrop",
        "background",
        "gravity",
        "move_speed",
        "jump_speed",
    ]

    def __init__(self, level_path, defaults):
        self._log = logging.getLogger(__name__)
        self._defaults = defaults

        self._level = self._load(level_path)
        self._collide_map, self._tiles = self.construct(self._level)

    def _load(self, level_path):
        """Loads a level from a JSON file."""
        self._log.debug(f"Loading level: {level_path!r}")

        # Read the file contents
        try:
            with open(level_path, "r") as level_file:
                level = json.load(level_file)

        except FileNotFoundError:
            raise LevelFileError(f"Cannot find level file: {level_path!r}.")
        except json.decoder.JSONDecodeError:
            raise LevelFileError(f"Level file {level_path!r} is not valid JSON.")

        # Check required attributes
        for attribute in self._required:
            if not attribute in level:
                if attribute in self._defaults:
                    level[attribute] = defaults[attribute].copy()
                else:
                    raise LevelFileError(
                        f"Level file {level_path!r} misses required attribute {attribute!r}."
                    )

        return level

    def construct(self, level):
        """Constructs tiles for the level."""

        return collide_map, tiles
