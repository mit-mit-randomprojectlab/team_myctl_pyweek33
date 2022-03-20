import pygame
import src.constants as constants


class ResourceManager:
    __images = dict()

    __sounds = dict()

    __resources_path = constants.RESOURCES_PATH

    def get_image(self, filename: str, reload: bool = False) -> pygame.surface.Surface:
        """Get Image

        Args:
            filename (str): filename to load
            reload (bool, optional): decides whether manager should return the cached image or reload it. Defaults to False.

        """
        # Check the path is defined
        if not ResourceManager.__resources_path:
            raise ValueError("Invalid resources path")

        # If using cache, and it cache, return cached image
        if not reload and filename in ResourceManager.__images:
            return ResourceManager.__images[filename]

        # Else, try to load the image
        try:
            image = pygame.image.load(
                ResourceManager.__resources_path / "gfx" / filename
            )

        except pygame.error as e:
            raise IOError("Couldn't load image: {e}".format(e=e))

        # If image has a transparent background, remove it
        if image.get_alpha():
            image = image.convert_alpha()
        else:
            image = image.convert()

        # Add to cached storage
        ResourceManager.__images[filename] = image

        return image

    # TODO: handle sound caching
    def get_sound(self, filename: str) -> pygame.mixer.Sound:
        ...

    def get_music(self, filename: str) -> pygame.mixer.Sound:
        ...
