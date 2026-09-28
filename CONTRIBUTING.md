# Contributing to PacMan

First off, thank you for considering contributing to **PacMan**! 🎮
Every contribution helps make this project better, whether it's a bug report, a feature request,
a documentation improvement, or a code change.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Features](#suggesting-features)
  - [Submitting Pull Requests](#submitting-pull-requests)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Style Guidelines](#style-guidelines)
- [Commit Convention](#commit-convention)
- [License](#license)

## Code of Conduct

This project and everyone participating in it are governed by the
[PacMan Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this
code. Please report unacceptable behavior to **[minigametech@proton.me](mailto:minigametech@proton.me)**.

## Getting Started

1. **Fork** the repository on GitHub.
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/<your-username>/PacMan.git
   cd PacMan
   ```
3. **Install dependencies**:
   ```bash
   pip install pygame
   ```
4. **Run the game** to verify everything works:
   ```bash
   python main.py
   ```

## How Can I Contribute?

### Reporting Bugs

If you find a bug, please [open an issue](https://github.com/minigame-tech/PacMan/issues/new)
and include:

- **A clear and descriptive title** for the issue.
- **Steps to reproduce** the behavior.
- **Expected behavior** — what you expected to happen.
- **Actual behavior** — what actually happened.
- **Screenshots or recordings**, if applicable.
- **Environment details**: OS, Python version (`python --version`), Pygame version.

### Suggesting Features

Feature requests are welcome! Please [open an issue](https://github.com/minigame-tech/PacMan/issues/new)
and include:

- **A clear and descriptive title** for the suggestion.
- **A detailed description** of the proposed feature and its expected behavior.
- **Why this feature would be useful** to the project.
- **Mockups or sketches**, if applicable (especially for UI changes).

### Submitting Pull Requests

1. **Create a branch** from `main` for your changes:
   ```bash
   git checkout -b feature/my-awesome-feature
   ```
2. **Make your changes** following the [Style Guidelines](#style-guidelines).
3. **Test your changes** thoroughly — launch the game and verify nothing is broken.
4. **Commit your changes** following the [Commit Convention](#commit-convention).
5. **Push** your branch and [open a Pull Request](https://github.com/minigame-tech/PacMan/pulls):
   ```bash
   git push origin feature/my-awesome-feature
   ```

> **Note**: Please open an issue first for significant changes so we can discuss the approach
> before you invest time in the implementation.

## Development Setup

### Prerequisites

| Tool   | Version  |
|--------|----------|
| Python | 3.8+     |
| Pygame | 2.x      |

### Running in Development

```bash
# Clone and enter the project
git clone https://github.com/minigame-tech/PacMan.git
cd PacMan

# Install dependencies
pip install pygame

# Launch the game
python main.py
```

### Building the Executable (Windows)

```bash
pip install pyinstaller
pyinstaller pacman.spec --noconfirm
# Output: dist/PacMan.exe
```

## Project Structure

```
PacMan/
├── main.py                   # Entry point and game loop
├── lib/
│   └── g2d.py                # Graphics and input library (Pygame wrapper)
├── src/
│   ├── Giocatore.py           # Player (Pac-Man) logic and rendering
│   └── Menu/
│       ├── __init__.py
│       └── Main_Menu.py       # Main menu UI
├── assets/
│   ├── img/                   # Sprites and background images
│   └── audio/                 # Sound effects
├── pacman.spec                # PyInstaller build spec
├── build_exe.bat              # Windows build script
├── LICENSE                    # MIT License
├── README.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md            # ← You are here
└── SECURITY.md
```

## Style Guidelines

### Python

- **Language**: Code identifiers (variables, functions, classes) are written in **Italian** to
  maintain consistency with the existing codebase.
- **PEP 8**: Follow [PEP 8](https://peps.python.org/pep-0008/) for formatting and style.
- **Type Hints**: Use type hints where possible. Avoid Python 3.10+ syntax (`X | Y`) to maintain
  backward compatibility — use `Optional[X]` or `Union[X, Y]` from `typing` instead.
- **Docstrings**: Use triple-quoted docstrings for all public classes and functions.
- **Line Length**: Keep lines under **100 characters** where practical.

### File Naming

- Python modules: `snake_case.py` (exception: `Giocatore.py`, `Main_Menu.py` — existing convention).
- Assets: descriptive names, lowercase with hyphens (e.g., `pac-man.png`).

## Commit Convention

We follow a simplified [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>: <short description>

[optional body with details]
```

### Types

| Type       | Description                                      |
|------------|--------------------------------------------------|
| `feat`     | A new feature                                    |
| `fix`      | A bug fix                                        |
| `docs`     | Documentation changes only                       |
| `style`    | Code style changes (formatting, no logic change) |
| `refactor` | Code refactoring (no feature or fix)             |
| `assets`   | New or updated game assets (images, audio)       |
| `build`    | Build system or dependency changes               |
| `chore`    | Maintenance tasks                                |

### Examples

```
feat: add power pellet mechanic with ghost vulnerability timer
fix: resolve tunnel wrap glitch when Pac-Man moves at high speed
docs: update README with new installation instructions
assets: add fruit bonus sprites to sprite sheet
```

## License

By contributing to PacMan, you agree that your contributions will be licensed under the
[MIT License](LICENSE) that covers the project.

---

Thank you for helping make PacMan better! 👾
