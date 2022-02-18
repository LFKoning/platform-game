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
        self._map = self._load(tile_path)

    def find(self, tile_code):
        """Looks up a tile code and returns its surface."""
        if tile_code not in self._map:
            self._error(f"Tile {tile_code!r} not found.")
        return self._map[tile_code]

    def _load(self, tile_path):
        """Loads a tileset from a JSON file."""
        self._log.debug(f"Loading tileset: {tile_path!r}")

        # Read the file contents
        try:
            with open(tile_path, "r") as tile_file:
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

        # Check tile dimensions
        width = tileset["tile_width"]
        try:
            width = int(width)
        except ValueError():
            self._error(f"Tileset {tile_path!r}: Width must be integer.")

        height = tileset["tile_height"]
        try:
            height = int(height)
        except ValueError():
            self._error(f"Tileset {tile_path!r}: Height must be integer.")

        # Check the tiles mapping
        if not isinstance(tileset["tiles"], dict):
            self._error(f"Tileset {tile_path!r}: Tiles must be a dictionary.")

        invalid = set(tileset["tiles"]) - self._valid_codes
        if invalid:
            self._error(
                f"Tileset {tile_path!r}: Contains invalid tile codes:"
                + ", ".join([repr(code) for code in invalid])
            )

        # Create the tiles
        tilemap = {}
        for code, image_path in tileset["tiles"].items():
            # Load tile image
            if image_path:
                try:
                    surface = pygame.image.load(image_path)
                    if surface.get_width() != width or surface.get_height() != height:
                        surface = pygame.transform.scale(surface, (width, height))
                except FileNotFoundError:
                    self._error(
                        f"Tileset {tile_path!r}: Cannot find tile image {image_path!r}."
                    )
                except pygame.error:
                    self._error(
                        f"Tileset {tile_path!r}: Invalid tile image {image_path!r}."
                    )

            # Create grey filler tile
            else:
                surface = pygame.Surface((width, height))
                surface.fill("grey")

            tilemap[code] = surface

        return tilemap

    def _error(self, msg):
        """Logs and handles exceptions."""
        self._log.error(msg)
        raise TilesetFileError(msg)
