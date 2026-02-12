"""Bullet sprites for player and alien projectiles."""

import arcade


class Bullet(arcade.Sprite):
    """
    A bullet that moves vertically up or down.

    Used by both player and alien entities.
    """

    def __init__(
        self,
        x: float,
        y: float,
        speed: float,
        is_player_bullet: bool = True,
        image_path: str | None = None,
    ) -> None:
        """
        Initialize a bullet.

        Args:
            x: Starting x coordinate.
            y: Starting y coordinate.
            speed: Speed of the bullet (positive for up, negative for down).
            is_player_bullet: True if player's bullet, False for alien bullet.
            image_path: Optional path to bullet sprite image.
        """
        if image_path:
            super().__init__(image_path, scale=0.5)
        else:
            color = arcade.color.YELLOW if is_player_bullet else arcade.color.RED
            texture = arcade.make_soft_square_texture(
                size=8,
                color=color,
                outer_alpha=255,
            )
            super().__init__(texture, scale=1.0)

        self.center_x = x
        self.center_y = y
        self.change_y = speed if is_player_bullet else -speed
        self.is_player_bullet = is_player_bullet

    def update(self, delta_time: float = 1 / 60) -> None:
        """
        Update bullet position.

        Args:
            delta_time: Time elapsed since last update in seconds.
        """
        self.center_y += self.change_y * delta_time

    def is_off_screen(self, screen_height: float) -> bool:
        """
        Check if bullet has left the screen.

        Args:
            screen_height: Height of the game screen.

        Returns:
            True if bullet is off screen.
        """
        return self.bottom > screen_height or self.top < 0
