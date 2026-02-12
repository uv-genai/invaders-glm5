"""Main entry point for the Invaders game."""

import arcade

from invaders.game import InvadersGame


def main() -> None:
    """
    Main entry point for the Invaders game.

    Creates the game window, sets up the game, and starts the game loop.
    """
    game = InvadersGame()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
