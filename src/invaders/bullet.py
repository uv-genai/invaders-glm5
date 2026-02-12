"""Bullet sprites for player and alien projectiles."""

import arcade

# Default sprite paths for bullets
PLAYER_BULLET_SPRITE = ":resources:/images/space_shooter/laserBlue01.png"
ALIEN_BULLET_SPRITE = ":resources:/images/space_shooter/laserRed01.png"


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
            sprite_path = image_path
        else:
            sprite_path = PLAYER_BULLET_SPRITE if is_player_bullet else ALIEN_BULLET_SPRITE

        super().__init__(sprite_path, scale=0.5)

        self.center_x = x
        self.center_y = y
        self.change_y = speed if is_player_bullet else -speed
        self.is_player_bullet = is_player_bullet

        # Rotate laser to point upward for player, downward for alien
        self.angle = 0 if is_player_bullet else 180

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
