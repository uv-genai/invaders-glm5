# Invaders

A Space Invaders clone built with the Python Arcade library.

## Installation

```bash
uv venv
uv pip install -e ".[dev]"
```

## Running the Game

```bash
uv run invaders
```

## Controls

- **Left/A**: Move left
- **Right/D**: Move right
- **Space**: Fire
- **R**: Restart (after game over)

## Development

### Code Quality

```bash
uv run ruff format .
uv run ruff check .
uv run mypy src/
```

### Testing

```bash
uv run pytest tests/ -v
```

## License

MIT
