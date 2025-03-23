"""Asset loader mixin class."""
import json
import pygame


class AssetMixin:

    def load_image(self, image_path):
        """Loads an image from file."""
        try:
            return pygame.image.load(image_path)
        except FileNotFoundError as error:
            raise FileNotFoundError(f"Cannot find tile image {image_path!r}.") from error
        except pygame.error as error:
            raise RuntimeError(f"Invalid tile image {image_path!r}.") from error

    def load_json(self, json_path, required=None):
        """Loads a JSON configuration file."""
        try:
            with open(json_path, "r", encoding="utf-8") as json_file:
                print("Loading: ", json_file)
                json_content = json.load(json_file)
        except FileNotFoundError as error:
            raise FileNotFoundError(f"Cannot find JSON file: {json_path!r}.") from error
        except json.decoder.JSONDecodeError as error:
            raise RuntimeError(f"Invalid JSON file: {json_path!r}.") from error

        # Check required keys
        if required:
            missing = required - set(json_content)
            if missing:
                RuntimeError(
                    "JSON file is missing the following attributes: "
                    + ", ".join([repr(v) for v in missing])
                )

        return json_content
