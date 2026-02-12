"""Alien enemy sprite and formation management."""

import random

import arcade

from invaders.bullet import Bullet
from invaders.settings import SETTINGS


class Alien(arcade.Sprite):
    """
    An alien enemy sprite.

    Aliens move horizontally in formation and occasionally shoot.
    """

    def __init__(
        self,
        x: float,
        y: float,
        alien_type: int = 0,
        image_path: str | None = None,
    ) -> None:
        """
        Initialize an alien.

        Args:
            x: Starting x coordinate.
            y: Starting y coordinate.
            alien_type: Type of alien (affects appearance/score).
            image_path: Optional path to alien sprite image.
        """
        if image_path:
            super().__init__(image_path, scale=0.5)
        else:
            colors = [arcade.color.PURPLE, arcade.color.BLUE, arcade.color.CYAN]
            color = colors[alien_type % len(colors)]
            texture = arcade.make_soft_square_texture(
                size=30,
                color=color,
                outer_alpha=255,
            )
            super().__init__(texture, scale=1.0)

        self.center_x = x
        self.center_y = y
        self.alien_type = alien_type
        self.change_x: float = SETTINGS.alien_speed
        self.change_y: float = 0.0

    def update(self, delta_time: float = 1 / 60) -> None:
        """
        Update alien position.

        Args:
            delta_time: Time elapsed since last update in seconds.
        """
        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time

    def drop_and_reverse(self) -> None:
        """Drop down and reverse horizontal direction."""
        self.center_y -= SETTINGS.alien_drop_distance
        self.change_x = -self.change_x


class AlienFormation:
    """
    Manages a formation of alien sprites.

    Handles movement, shooting, and collision detection for all aliens.
    """

    def __init__(self) -> None:
        """Initialize an empty alien formation."""
        self.aliens: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()
        self.bullets: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()
        self._move_down: bool = False

    def create_formation(self) -> None:
        """Create the initial alien formation based on settings."""
        start_x = (
            SETTINGS.screen_width - (SETTINGS.alien_columns - 1) * SETTINGS.alien_spacing
        ) / 2
        start_y = SETTINGS.screen_height - 100

        for row in range(SETTINGS.alien_rows):
            for col in range(SETTINGS.alien_columns):
                x = start_x + col * SETTINGS.alien_spacing
                y = start_y - row * SETTINGS.alien_spacing
                alien = Alien(x, y, alien_type=row)
                self.aliens.append(alien)

    def update(self, delta_time: float = 1 / 60) -> None:
        """
        Update all aliens and their bullets.

        Args:
            delta_time: Time elapsed since last update in seconds.
        """
        # Check if any alien hit the edge
        self._move_down = False
        for alien in self.aliens:
            if alien.right >= SETTINGS.screen_width or alien.left <= 0:
                self._move_down = True
                break

        # Update aliens
        for alien in self.aliens:
            if self._move_down:
                if isinstance(alien, Alien):
                    alien.drop_and_reverse()
            alien.update(delta_time)

        # Update bullets
        self.bullets.update(delta_time)

        # Remove off-screen bullets
        for bullet in list(self.bullets):
            if isinstance(bullet, Bullet) and bullet.is_off_screen(SETTINGS.screen_height):
                bullet.remove_from_sprite_lists()

    def maybe_shoot(self, shoot_chance: float = 0.01) -> Bullet | None:
        """
        Randomly shoot a bullet from a random alien.

        Args:
            shoot_chance: Probability of shooting per frame.

        Returns:
            A new bullet if one was fired, None otherwise.
        """
        if random.random() < shoot_chance and len(self.aliens) > 0:
            shooter = random.choice(list(self.aliens))
            bullet = Bullet(
                x=shooter.center_x,
                y=shooter.bottom,
                speed=SETTINGS.alien_bullet_speed,
                is_player_bullet=False,
            )
            self.bullets.append(bullet)
            return bullet
        return None

    def remove_dead_aliens(self) -> None:
        """Remove all aliens marked for removal."""
        self.aliens = [a for a in self.aliens if not a.removed]  # type: ignore
        if hasattr(self.aliens, "update"):
            self.aliens = arcade.SpriteList()
            # Re-add surviving aliens
            pass

    def is_empty(self) -> bool:
        """
        Check if all aliens have been destroyed.

        Returns:
            True if no aliens remain.
        """
        return len(self.aliens) == 0

    def reached_bottom(self, y_threshold: float = 100.0) -> bool:
        """
        Check if any alien has reached the bottom of the screen.

        Args:
            y_threshold: Y coordinate threshold (player area).

        Returns:
            True if any alien has descended below threshold.
        """
        for alien in self.aliens:
            if alien.bottom < y_threshold:
                return True
        return False
