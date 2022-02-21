"""Module for the Tileset class."""
import json
import string
import logging

import pygame


class TilesetFileError(Exception):
    """Raised when the tileset file contains errors."""


class Tileset:
    """Tileset class that maps tile codes to sprites."""

    _required = set(("tile_width", "tile_height", "tiles"))
    _valid_codes = set(string.ascii_letters + string.digits)

    def __init__(self, tile_path):
        self._log = logging.getLogger(__name__)

        tileset = self._load_file(tile_path)
        self.tile_width, self.tile_height = self._get_dimensions(tileset)
        self._map = self._construct_map(tileset)

    def find(self, tile_code):
        """Looks up a tile code and returns its surface."""
        if tile_code not in self._map:
            self._error(f"Tile {tile_code!r} not found.")
        return self._map[tile_code]

    def _load_file(self, tile_path):
        """Loads a tileset from a JSON file."""
        self._log.debug(f"Loading tileset: {tile_path!r}")

        # Read the file contents
        try:
            with open(tile_path, "r", encoding="utf-8") as tile_file:
                tileset = json.load(tile_file)

        except FileNotFoundError:
            self._error(f"Tileset {tile_path!r}: Cannot find the file.")
        except json.decoder.JSONDecodeError:
            self._error(f"Tileset {tile_path!r}: Invalid JSON file.")

        # Check required keys
        missing = self._required - set(tileset)
        if missing:
            self._error(
                "Tileset is missing attributes: "
                + ", ".join([repr(v) for v in missing])
            )

        return tileset

    def _get_dimensions(self, tileset):
        """Gets tile dimensions from the tileset."""

        try:
            width = int(tileset["tile_width"])
        except ValueError():
            self._error(f"Tile width must be integer.")

        try:
            height = int(tileset["tile_height"])
        except ValueError():
            self._error(f"Tile height must be integer.")

        return width, height

    def _construct_map(self, tileset):
        """Creates the tiles specification."""

        # Check the tiles mapping
        if not isinstance(tileset["tiles"], dict):
            self._error(f"Tileset must specify tiles as a dictionary.")

        invalid = set(tileset["tiles"]) - self._valid_codes
        if invalid:
            self._error(
                f"Tileset contains invalid tile codes:"
                + ", ".join([repr(code) for code in invalid])
            )

        tilemap = {}
        for code, properties in tileset["tiles"].items():
            # Load tile image
            if "image" in properties:
                image_path = properties["image"]
                try:
                    surface = pygame.image.load(image_path)
                    surface = pygame.transform.scale(
                        surface, (self.tile_width, self.tile_height)
                    )
                except FileNotFoundError:
                    self._error(f"Cannot find tile image {image_path!r}.")
                except pygame.error:
                    self._error(f"Invalid tile image {image_path!r}.")

            # Create grey filler tile
            else:
                surface = pygame.Surface((self.tile_width, self.tile_height))
                surface.fill("grey")

            properties["image"] = surface
            tilemap[code] = properties

        return tilemap

    def _error(self, msg):
        """Logs and handles exceptions."""
        self._log.error(msg)
        raise TilesetFileError(msg)


class Tile(pygame.sprite.Sprite):
    """Class for handling a single tile."""

    def __init__(self, x, y, properties):

        super().__init__()
        self.image = properties["image"]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.offset = pygame.Vector2(0, 0)

    def __getattr__(self, attribute):
        """Re-map Rect attributes."""
        if hasattr(self.rect, attribute):
            return getattr(self.rect, attribute)
        else:
            raise AttributeError(
                f"Tile has no attribute {attribute!r}."
            )

    def update(self, x, y):
        """Moves tile by the given offset."""
        self.offset.x = x
        self.offset.y = y

        self.rect.x = self.offset.x + self.rect.x
        self.rect.y = self.offset.y + self.rect.y
