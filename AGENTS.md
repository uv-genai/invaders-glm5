# AGENTS.md

> Coding agent documentation for the Invaders project.

## Project Overview

**Invaders** is a Space Invaders clone built with Python and the Arcade library. It features sprite-based graphics, explosion animations, sound effects, and a parallax starfield background.

- **Version**: 0.6.0
- **Repository**: https://github.com/uv-genai/invaders-glm5
- **Language**: Python 3.14+
- **Game Engine**: Arcade 3.3+

## Quick Start

```bash
# Clone the repository
git clone https://github.com/uv-genai/invaders-glm5.git
cd invaders-glm5

# Create virtual environment and install dependencies
uv venv
uv pip install -e ".[dev]"

# Run the game
uv run invaders
```

## Controls

| Key | Action |
|-----|--------|
| Left / A | Move left |
| Right / D | Move right |
| Space | Fire |
| F | Toggle fullscreen |
| R | Restart (after game over) |

## Project Structure

```
invaders/
├── pyproject.toml          # Project configuration and dependencies
├── README.md               # User documentation
├── AGENTS.md               # This file - agent documentation
├── src/
│   └── invaders/
│       ├── __init__.py     # Package initialization, version
│       ├── main.py         # Entry point
│       ├── game.py         # Main game class (InvadersGame)
│       ├── player.py       # Player spaceship sprite
│       ├── alien.py        # Alien sprites and formation management
│       ├── bullet.py       # Player and alien bullet sprites
│       ├── explosion.py    # Explosion animation sprite
│       ├── star.py         # Parallax starfield background
│       └── settings.py     # Game configuration constants
└── tests/                  # Unit tests (if any)
```

## Architecture

### Game Flow

```
main.py
    └── InvadersGame (arcade.Window)
            ├── setup()         # Initialize/reset game state
            ├── on_draw()       # Render frame
            ├── on_update()     # Update game logic (60 FPS)
            └── on_key_press()  # Handle input
```

### Class Hierarchy

```
arcade.Window
    └── InvadersGame
            ├── Camera2D (viewport/projection for fullscreen scaling)
            ├── StarField
            │       └── StarLayer[] (far, mid, near)
            │               └── Star[]
            ├── Player (arcade.Sprite)
            ├── AlienFormation
            │       ├── Alien[] (arcade.Sprite)
            │       └── Bullet[] (alien bullets)
            └── Bullet[] (player bullets)
```

### Key Classes

#### `InvadersGame` (game.py)
- Main game window inheriting from `arcade.Window`
- Manages game state, rendering, and input
- Uses `Camera2D` for proper fullscreen scaling with fixed game coordinates
- **Important**: Always use `self.camera.use()` before drawing

#### `Player` (player.py)
- Player-controlled spaceship sprite
- Properties: `lives`, `change_x` (horizontal velocity)
- Methods: `move_left()`, `move_right()`, `stop()`, `hit()`, `is_alive()`

#### `Alien` / `AlienFormation` (alien.py)
- `Alien`: Individual enemy sprite with movement and shooting
- `AlienFormation`: Manages group of aliens, handles formation movement and shooting
- Aliens move horizontally, drop down when hitting screen edges

#### `Bullet` (bullet.py)
- Projectile sprite used by both player and aliens
- `is_player_bullet` flag determines direction and appearance
- Auto-removes when off-screen

#### `Explosion` (explosion.py)
- Animated explosion using spritesheet frames
- Self-removes from sprite lists when animation completes
- Uses `load_explosion_textures()` to load from Arcade resources

#### `StarField` / `Star` / `StarLayer` (star.py)
- Parallax background with 3 layers (far/mid/near)
- Stars scroll downward at different speeds for depth effect
- Far: slow, dim, many | Near: fast, bright, few

### Settings (settings.py)

All game constants are centralized in `GameSettings` dataclass:

```python
@dataclass(frozen=True)
class GameSettings:
    screen_width: int = 800
    screen_height: int = 600
    player_speed: float = 300.0
    player_lives: int = 3
    bullet_speed: float = 500.0
    alien_speed: float = 100.0
    alien_rows: int = 5
    alien_columns: int = 10
    ...
```

Access via `SETTINGS` singleton instance.

## Dependencies

| Package | Purpose |
|---------|---------|
| arcade | Game engine, rendering, sprites |
| ruff | Linting and formatting (dev) |
| mypy | Type checking (dev) |
| pytest | Testing (dev) |

## Code Style Guidelines

- **Type hints**: Required on all functions and methods
- **Docstrings**: Required for all public APIs
- **Formatting**: ruff (PEP8, line length 100)
- **Type checking**: mypy strict mode
- **No global variables**: Use dataclasses for settings

### Before Committing

```bash
# Format and lint
uv run ruff format .
uv run ruff check .

# Type check
uv run mypy src/

# Syntax check
uv run -m py_compile src/invaders/*.py
```

## Asset Sources

All sprites and sounds use Arcade's built-in resources from Kenney.nl (CC0 license):

| Asset Type | Resource Path |
|------------|---------------|
| Player ship | `:resources:/images/space_shooter/playerShip1_orange.png` |
| Aliens | `:resources:/images/enemies/slime*.png`, `worm*.png` |
| Player bullet | `:resources:/images/space_shooter/laserBlue01.png` |
| Alien bullet | `:resources:/images/space_shooter/laserRed01.png` |
| Explosion | `:resources:/images/spritesheets/explosion.png` |
| Sounds | `:resources:/sounds/laser1.wav`, `explosion2.wav`, etc. |

## Common Tasks

### Adding a New Sprite Type

1. Create class inheriting from `arcade.Sprite`
2. Load texture in `__init__` using `arcade.load_texture()` or create programmatically
3. Add to appropriate `SpriteList` in `InvadersGame`
4. Update in `on_update()`, draw in `on_draw()`

### Adding a New Sound Effect

1. Load sound: `self.sound = arcade.load_sound(":resources:/sounds/name.wav")`
2. Play sound: `arcade.play_sound(self.sound)`

### Modifying Game Difficulty

Edit `src/invaders/settings.py` to adjust:
- `alien_speed`, `alien_rows`, `alien_columns`
- `alien_shoot_interval`, `alien_bullet_speed`
- `player_lives`, `bullet_speed`

## Troubleshooting

### Game window is black
- Ensure `self.camera.use()` is called before drawing
- Check that sprites are added to SpriteLists

### Fullscreen doesn't scale properly
- Camera viewport should be `self.rect`, projection should be fixed to game dimensions
- Call `self.camera.viewport = self.rect` after `set_fullscreen()`

### Sprites not visible
- Check sprite has valid texture
- Verify sprite is added to a SpriteList
- Ensure SpriteList.draw() is called in on_draw()

## Changelog

### v0.6.0 (Uncommitted)
- Added parallax starfield background with 3 layers
- Stars scroll at different speeds for depth effect

### v0.5.0 (Uncommitted)
- Fixed fullscreen scaling with Camera2D
- Allow F key to toggle fullscreen during game over

### v0.4.0
- Added fullscreen toggle with F key

### v0.3.0
- Added sound effects:
  - Laser sound on player shoot
  - Explosion sound on alien destruction
  - Hit sound when player is hit
  - Game over sound on loss
  - Victory sound on win

### v0.2.0
- Replaced colored shapes with sprite graphics
- Added explosion animation using spritesheet
- Player ship: orange spaceship
- Aliens: various slimes and worms
- Bullets: blue/red lasers

### v0.1.0
- Initial implementation
- Basic Space Invaders gameplay
- Player movement and shooting
- Alien formation movement and shooting
- Collision detection
- Score and lives system
- Game over and victory screens
