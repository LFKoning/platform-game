"""Asset loader mixin class."""
import json
import pygame


class AssetMixin:

    def load_image(self, image_path):
        """Loads an image from file."""
        try:
            return pygame.image.load(image_path)
        except FileNotFoundError:
            FileNotFoundError(f"Cannot find tile image {image_path!r}.")
        except pygame.error:
            RuntimeError(f"Invalid tile image {image_path!r}.")

    def load_json(self, json_path, required = None):
        """Loads a JSON configuration file."""
        try:
            with open(json_path, "r", encoding="utf-8") as json_file:
                json_cfg = json.load(json_file)
        except FileNotFoundError:
            FileNotFoundError(f"Cannot find JSON file: {json_path!r}.")
        except json.decoder.JSONDecodeError:
            RuntimeError(f"Invalid JSON file: {json_path!r}.")

        # Check required keys
        if required:
            missing = required - set(json_cfg)
            if missing:
                RuntimeError(
                    "JSON file is missing the following attributes: "
                    + ", ".join([repr(v) for v in missing])
                )

        return json_cfg
