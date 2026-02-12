"""Game configuration and constants."""

from dataclasses import dataclass


@dataclass(frozen=True)
class GameSettings:
    """Immutable game settings and configuration."""

    # Screen dimensions
    screen_width: int = 800
    screen_height: int = 600
    screen_title: str = "Invaders"

    # Player settings
    player_speed: float = 300.0
    player_lives: int = 3

    # Bullet settings
    bullet_speed: float = 500.0
    bullet_scale: float = 0.5

    # Alien settings
    alien_speed: float = 100.0
    alien_drop_distance: float = 50.0
    alien_rows: int = 5
    alien_columns: int = 10
    alien_spacing: float = 60.0

    # Game settings
    alien_shoot_interval: float = 2.0
    alien_bullet_speed: float = 300.0


# Default game settings instance
SETTINGS = GameSettings()
