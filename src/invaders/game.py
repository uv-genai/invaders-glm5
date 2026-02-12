"""Main game class managing the Space Invaders game."""

import arcade

from invaders.alien import AlienFormation
from invaders.bullet import Bullet
from invaders.player import Player
from invaders.settings import SETTINGS


class InvadersGame(arcade.Window):
    """
    Main Space Invaders game class.

    Manages game state, rendering, and player input.
    """

    def __init__(self) -> None:
        """
        Initialize the game window and set up game objects.

        Creates the window with dimensions from settings and initializes
        sprite lists for player, aliens, and bullets.
        """
        super().__init__(
            width=SETTINGS.screen_width,
            height=SETTINGS.screen_height,
            title=SETTINGS.screen_title,
        )

        # Game objects
        self.player: Player
        self.player_list: arcade.SpriteList[arcade.Sprite]
        self.alien_formation: AlienFormation
        self.player_bullets: arcade.SpriteList[arcade.Sprite]

        # Game state
        self.score: int = 0
        self.game_over: bool = False
        self.game_won: bool = False

        # Background color
        self.background_color = arcade.color.BLACK

    def setup(self) -> None:
        """
        Set up a new game.

        Initializes or resets all game objects and state. Call this
        to start a new game or restart after game over.
        """
        # Create player at bottom center of screen
        self.player = Player()
        self.player.center_x = SETTINGS.screen_width / 2
        self.player.center_y = 50

        # Create player sprite list
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        # Create alien formation
        self.alien_formation = AlienFormation()
        self.alien_formation.create_formation()

        # Create player bullet list
        self.player_bullets = arcade.SpriteList()

        # Reset game state
        self.score = 0
        self.game_over = False
        self.game_won = False

    def on_draw(self) -> None:
        """Render the game screen."""
        self.clear()

        # Draw game objects
        self.player_list.draw()
        self.alien_formation.aliens.draw()
        self.alien_formation.bullets.draw()
        self.player_bullets.draw()

        # Draw UI
        self._draw_ui()

        # Draw game over or win screen
        if self.game_over:
            self._draw_game_over()
        elif self.game_won:
            self._draw_victory()

    def on_update(self, delta_time: float) -> None:
        """
        Update game logic.

        Args:
            delta_time: Time elapsed since last update in seconds.
        """
        if self.game_over or self.game_won:
            return

        # Update player
        self.player.update(delta_time)

        # Update aliens
        self.alien_formation.update(delta_time)
        self.alien_formation.maybe_shoot(shoot_chance=0.02)

        # Update player bullets
        self.player_bullets.update(delta_time)

        # Remove off-screen player bullets
        for bullet in list(self.player_bullets):
            if isinstance(bullet, Bullet) and bullet.is_off_screen(SETTINGS.screen_height):
                bullet.remove_from_sprite_lists()

        # Check collisions
        self._check_collisions()

        # Check win/lose conditions
        self._check_game_state()

    def on_key_press(self, key: int, modifiers: int) -> None:
        """
        Handle key press events.

        Args:
            key: The key that was pressed.
            modifiers: Bitwise OR of modifier keys pressed.
        """
        if self.game_over or self.game_won:
            if key == arcade.key.R:
                self.setup()
            return

        match key:
            case arcade.key.LEFT | arcade.key.A:
                self.player.move_left()
            case arcade.key.RIGHT | arcade.key.D:
                self.player.move_right()
            case arcade.key.SPACE:
                self._fire_player_bullet()

    def on_key_release(self, key: int, modifiers: int) -> None:
        """
        Handle key release events.

        Args:
            key: The key that was released.
            modifiers: Bitwise OR of modifier keys still pressed.
        """
        match key:
            case arcade.key.LEFT | arcade.key.A if self.player.change_x < 0:
                self.player.stop()
            case arcade.key.RIGHT | arcade.key.D if self.player.change_x > 0:
                self.player.stop()

    def _fire_player_bullet(self) -> None:
        """Fire a bullet from the player's position."""
        # Limit to one player bullet at a time (classic Space Invaders behavior)
        if len(self.player_bullets) < 3:
            bullet = Bullet(
                x=self.player.center_x,
                y=self.player.top,
                speed=SETTINGS.bullet_speed,
                is_player_bullet=True,
            )
            self.player_bullets.append(bullet)

    def _check_collisions(self) -> None:
        """Check and handle all sprite collisions."""
        # Player bullets hitting aliens
        for bullet in list(self.player_bullets):
            if isinstance(bullet, Bullet):
                hit_aliens = arcade.check_for_collision_with_list(
                    bullet,
                    self.alien_formation.aliens,
                )
                for alien in hit_aliens:
                    # Remove bullet and alien
                    bullet.remove_from_sprite_lists()
                    alien.remove_from_sprite_lists()
                    # Update score
                    self.score += 10
                    break

        # Alien bullets hitting player
        for bullet in list(self.alien_formation.bullets):
            if isinstance(bullet, Bullet):
                if arcade.check_for_collision(bullet, self.player):
                    bullet.remove_from_sprite_lists()
                    self.player.hit()
                    if not self.player.is_alive():
                        self.game_over = True

        # Aliens colliding with player
        if arcade.check_for_collision_with_list(
            self.player,
            self.alien_formation.aliens,
        ):
            self.game_over = True

    def _check_game_state(self) -> None:
        """Check for win/lose conditions."""
        # Win: all aliens destroyed
        if self.alien_formation.is_empty():
            self.game_won = True

        # Lose: aliens reached the bottom
        if self.alien_formation.reached_bottom(y_threshold=80):
            self.game_over = True

    def _draw_ui(self) -> None:
        """Draw score and lives display."""
        # Draw score
        arcade.draw_text(
            text=f"Score: {self.score}",
            x=10,
            y=SETTINGS.screen_height - 30,
            color=arcade.color.WHITE,
            font_size=16,
        )

        # Draw lives
        arcade.draw_text(
            text=f"Lives: {self.player.lives}",
            x=10,
            y=SETTINGS.screen_height - 50,
            color=arcade.color.WHITE,
            font_size=16,
        )

    def _draw_game_over(self) -> None:
        """Draw game over screen."""
        arcade.draw_text(
            text="GAME OVER",
            x=SETTINGS.screen_width / 2,
            y=SETTINGS.screen_height / 2 + 30,
            color=arcade.color.RED,
            font_size=40,
            anchor_x="center",
        )
        arcade.draw_text(
            text=f"Final Score: {self.score}",
            x=SETTINGS.screen_width / 2,
            y=SETTINGS.screen_height / 2 - 10,
            color=arcade.color.WHITE,
            font_size=20,
            anchor_x="center",
        )
        arcade.draw_text(
            text="Press R to Restart",
            x=SETTINGS.screen_width / 2,
            y=SETTINGS.screen_height / 2 - 40,
            color=arcade.color.YELLOW,
            font_size=16,
            anchor_x="center",
        )

    def _draw_victory(self) -> None:
        """Draw victory screen."""
        arcade.draw_text(
            text="YOU WIN!",
            start_x=SETTINGS.screen_width / 2,
            start_y=SETTINGS.screen_height / 2 + 30,
            color=arcade.color.GREEN,
            font_size=40,
            anchor_x="center",
        )
        arcade.draw_text(
            text=f"Final Score: {self.score}",
            start_x=SETTINGS.screen_width / 2,
            start_y=SETTINGS.screen_height / 2 - 10,
            color=arcade.color.WHITE,
            font_size=20,
            anchor_x="center",
        )
        arcade.draw_text(
            text="Press R to Play Again",
            start_x=SETTINGS.screen_width / 2,
            start_y=SETTINGS.screen_height / 2 - 40,
            color=arcade.color.YELLOW,
            font_size=16,
            anchor_x="center",
        )
