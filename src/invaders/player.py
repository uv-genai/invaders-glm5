"""Player spaceship sprite."""

import arcade

from invaders.settings import SETTINGS


class Player(arcade.Sprite):
    """
    Player-controlled spaceship sprite.

    The player can move left and right and shoot bullets at the aliens.
    """

    def __init__(self, image_path: str | None = None) -> None:
        """
        Initialize the player sprite.

        Args:
            image_path: Optional path to player sprite image. Uses default if None.
        """
        if image_path:
            super().__init__(image_path, scale=0.5)
        else:
            # Create a solid color texture and use it for the sprite
            texture = arcade.make_soft_square_texture(
                size=40,
                color=arcade.color.GREEN,
                outer_alpha=255,
            )
            super().__init__(texture, scale=1.0)

        self.lives: int = SETTINGS.player_lives
        self.change_x: float = 0.0

    def update(self, delta_time: float = 1 / 60) -> None:
        """
        Update player position based on velocity.

        Args:
            delta_time: Time elapsed since last update in seconds.
        """
        # Move the player
        self.center_x += self.change_x * delta_time

        # Keep player on screen
        if self.left < 0:
            self.left = 0
        elif self.right > SETTINGS.screen_width:
            self.right = SETTINGS.screen_width

    def move_left(self) -> None:
        """Start moving left."""
        self.change_x = -SETTINGS.player_speed

    def move_right(self) -> None:
        """Start moving right."""
        self.change_x = SETTINGS.player_speed

    def stop(self) -> None:
        """Stop horizontal movement."""
        self.change_x = 0.0

    def hit(self) -> None:
        """Handle being hit by enemy bullet."""
        self.lives -= 1

    def is_alive(self) -> bool:
        """
        Check if player still has lives.

        Returns:
            True if player has remaining lives.
        """
        return self.lives > 0
