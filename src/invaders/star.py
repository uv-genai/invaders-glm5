"""Parallax starfield background with multiple layers."""

import random

import arcade

from invaders.settings import SETTINGS


class Star(arcade.Sprite):
    """
    A single star sprite that moves downward to create scrolling effect.

    When the star exits the bottom of the screen, it wraps to the top.
    """

    def __init__(
        self, x: float, y: float, size: int, speed: float, color: tuple[int, int, int, int]
    ) -> None:
        """
        Initialize a star.

        Args:
            x: Starting x coordinate.
            y: Starting y coordinate.
            size: Size of the star in pixels.
            speed: Downward movement speed in pixels per second.
            color: RGBA color tuple for the star.
        """
        # Create a soft circular texture for the star
        texture = arcade.make_circle_texture(size, color)
        super().__init__(texture, scale=1.0)

        self.center_x = x
        self.center_y = y
        self.speed = speed

    def update(self, delta_time: float = 1 / 60) -> None:
        """
        Update star position.

        Args:
            delta_time: Time elapsed since last update in seconds.
        """
        self.center_y -= self.speed * delta_time

        # Wrap around: if star goes below screen, move to top
        if self.bottom < 0:
            self.top = SETTINGS.screen_height


class StarLayer:
    """
    A layer of stars all moving at the same speed.

    Multiple layers at different speeds create parallax depth effect.
    """

    def __init__(
        self,
        count: int,
        size_range: tuple[int, int],
        speed: float,
        color: tuple[int, int, int, int],
    ) -> None:
        """
        Initialize a star layer.

        Args:
            count: Number of stars in this layer.
            size_range: (min_size, max_size) for random star sizes.
            speed: Movement speed for all stars in this layer.
            color: RGBA color tuple for stars in this layer.
        """
        self.stars: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()

        for _ in range(count):
            x = random.uniform(0, SETTINGS.screen_width)
            y = random.uniform(0, SETTINGS.screen_height)
            size = random.randint(size_range[0], size_range[1])

            star = Star(x, y, size, speed, color)
            self.stars.append(star)

    def update(self, delta_time: float = 1 / 60) -> None:
        """
        Update all stars in this layer.

        Args:
            delta_time: Time elapsed since last update in seconds.
        """
        for star in self.stars:
            if isinstance(star, Star):
                star.update(delta_time)

    def draw(self) -> None:
        """Render all stars in this layer."""
        self.stars.draw()


class StarField:
    """
    Multi-layer parallax starfield background.

    Contains three layers (far, mid, near) moving at different speeds
    to create an illusion of depth in space.
    """

    def __init__(self) -> None:
        """Initialize the starfield with three parallax layers."""
        # Far layer: many tiny dim stars, slow movement
        self.far_layer = StarLayer(
            count=150,
            size_range=(1, 2),
            speed=15.0,
            color=(128, 128, 128, 128),  # Gray, semi-transparent
        )

        # Mid layer: medium stars, medium speed
        self.mid_layer = StarLayer(
            count=100,
            size_range=(2, 3),
            speed=40.0,
            color=(200, 200, 255, 180),  # Light blue, mostly opaque
        )

        # Near layer: fewer bright stars, fast movement
        self.near_layer = StarLayer(
            count=50,
            size_range=(3, 4),
            speed=80.0,
            color=(255, 255, 255, 255),  # White, fully opaque
        )

    def update(self, delta_time: float = 1 / 60) -> None:
        """
        Update all star layers.

        Args:
            delta_time: Time elapsed since last update in seconds.
        """
        self.far_layer.update(delta_time)
        self.mid_layer.update(delta_time)
        self.near_layer.update(delta_time)

    def draw(self) -> None:
        """Render all star layers from far to near."""
        self.far_layer.draw()
        self.mid_layer.draw()
        self.near_layer.draw()
