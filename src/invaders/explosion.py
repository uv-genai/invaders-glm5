"""Explosion animation sprite."""

import arcade


class Explosion(arcade.Sprite):
    """
    An explosion animation that plays through multiple texture frames.

    When the animation completes, the sprite removes itself from all sprite lists.
    """

    def __init__(self, texture_list: list[arcade.Texture], x: float, y: float) -> None:
        """
        Initialize an explosion animation.

        Args:
            texture_list: List of textures representing explosion animation frames.
            x: X coordinate for explosion center.
            y: Y coordinate for explosion center.
        """
        super().__init__(texture_list[0], scale=0.5)

        self.center_x = x
        self.center_y = y

        # Animation state
        self.time_elapsed: float = 0.0
        self.current_texture: int = 0
        self.textures: list[arcade.Texture] = texture_list

    def update(self, delta_time: float = 1 / 60) -> None:
        """
        Update the explosion animation.

        Args:
            delta_time: Time elapsed since last update in seconds.
        """
        self.time_elapsed += delta_time

        # Update to the next frame of the animation
        # Use 60 FPS as base animation speed
        self.current_texture = int(self.time_elapsed * 60)

        if self.current_texture < len(self.textures):
            self.texture = self.textures[self.current_texture]
        else:
            # Animation complete, remove sprite
            self.remove_from_sprite_lists()


def load_explosion_textures() -> list[arcade.Texture]:
    """
    Load explosion animation textures from the spritesheet.

    Returns:
        List of Texture objects representing explosion frames.
    """
    columns = 16
    count = 60
    sprite_width = 256
    sprite_height = 256
    file_name = ":resources:/images/spritesheets/explosion.png"

    spritesheet = arcade.load_spritesheet(file_name)
    texture_list = spritesheet.get_texture_grid(
        size=(sprite_width, sprite_height),
        columns=columns,
        count=count,
    )

    return texture_list
