"""Module for the Tileset class."""
import json
import string
import logging

import pygame

from game.assets import AssetMixin


class TilesetFileError(Exception):
    """Raised when the tileset file contains errors."""


class Tileset(AssetMixin):
    """Tileset class that maps tile codes to sprites."""

    _required = set(("tile_width", "tile_height", "tiles"))
    _valid_codes = set(string.ascii_letters + string.digits)

    def __init__(self, tile_path):
        self._log = logging.getLogger(__name__)

        tileset = self.load_json(tile_path)
        self.tile_width, self.tile_height = self.get_dimensions(tileset)
        self._map = self.construct_mapping(tileset)

    def find(self, tile_code):
        """Looks up a tile code and returns its surface."""
        if tile_code not in self._map:
            self._error(f"Tile {tile_code!r} not found.")
        return self._map[tile_code]

    def get_dimensions(self, tileset):
        """Gets tile dimensions from the tileset."""

        try:
            width = int(tileset["tile_width"])
        except ValueError():
            self._error(f"Tile width must be integer, got {tileset['tile_width']!r}.")

        try:
            height = int(tileset["tile_height"])
        except ValueError():
            self._error(f"Tile height must be integer, got {tileset['tile_width']!r}.")

        return width, height

    def construct_mapping(self, tileset):
        """Creates the tiles specification."""

        # Check the tiles mapping
        if not isinstance(tileset["tiles"], dict):
            self._error("Tileset must specify tiles as a dictionary.")

        invalid = set(tileset["tiles"]) - self._valid_codes
        if invalid:
            self._error(
                "Tileset contains invalid tile codes:"
                + ", ".join([repr(code) for code in invalid])
            )

        tilemap = {}
        for code, properties in tileset["tiles"].items():

            self._log.debug(f"Processing tile {code}: {properties}.")
            # Load tile image
            if "image" in properties:
                surface = self.load_image(properties["image"])
            # Create grey filler tile
            else:
                surface = pygame.Surface((self.tile_width, self.tile_height))
                surface.fill("grey")

            # Add an overlay image
            overlay = properties.get("overlay", None)
            if overlay:
                offset = overlay.get("offset", (0, 0))
                overlay = self.load_image(overlay["image"])
                surface.blit(overlay, offset)

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

    def __getattr__(self, attribute):
        """Re-map Rect attributes."""
        if hasattr(self.rect, attribute):
            return getattr(self.rect, attribute)
        raise AttributeError(f"Tile has no attribute {attribute!r}.")
