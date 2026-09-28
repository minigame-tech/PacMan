# 👻 Pac-Man: Python Remake

![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)

A faithful remake of the classic arcade game **Pac-Man**, developed entirely in **Python**. 
The project leverages **Pygame** for the audio engine and the custom **g2d** module to handle the graphical rendering and core game loops in a lightweight, structured manner.

<!-- 
TIPS: Add a gameplay screenshot or GIF here! 
![Gameplay Screenshot](assets/img/gameplay-preview.png)
-->

## 🚀 Key Features

*   **Classic Gameplay**: Mechanics faithful to the original arcade version, including Pac-Man's movement, maze wrap-around (tunnels), dot consumption, and enemy ghost behaviors.
*   **Dynamic Audio**: Authentic sound effects managed via Pygame for an immersive retro experience.
*   **Lightweight Engine**: Built on the custom `g2d` library for simplified graphical rendering and input management.
*   **Cross-Platform & Standalone**: Playable directly via Python source code or compilable into a standalone `.exe` for Windows.

## 🎮 How to Play

*   **Movement**: <kbd>↑</kbd> <kbd>↓</kbd> <kbd>←</kbd> <kbd>→</kbd> or <kbd>W</kbd> <kbd>A</kbd> <kbd>S</kbd> <kbd>D</kbd>
*   **Select/Confirm**: <kbd>Enter</kbd>
*   **Objective**: Eat all the dots in the maze to win while avoiding the colorful ghosts. If they catch you, you lose a life!

## 🛠️ Installation & Getting Started

### Option 1: Play from Source (Cross-Platform)
Ensure you have Python 3.8+ installed, then follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/minigame-tech/PacMan.git
   cd PacMan
   ```
2. Install the required dependencies:
   ```bash
   pip install pygame
   ```
3. Run the game:
   ```bash
   python main.py
   ```

### Option 2: Standalone Executable (Windows)
You can build a standalone executable that doesn't require Python to be installed on the target machine.

1. Double-click the included `build_exe.bat` script.
   *(Alternatively, run `pip install pyinstaller pygame` and `pyinstaller pacman.spec --noconfirm` in your terminal).*
2. Navigate to the `dist/` folder.
3. Launch `PacMan.exe` and enjoy!

## 🤝 Community & Contributing

We welcome contributions of all kinds—whether it's reporting bugs, suggesting new features, or submitting pull requests!

*   **[Contributing Guide](CONTRIBUTING.md)**: Learn how to set up the project and submit changes.
*   **[Code of Conduct](CODE_OF_CONDUCT.md)**: Our community standards and expectations.
*   **[Security Policy](SECURITY.md)**: How to responsibly report security vulnerabilities.

## 📈 Roadmap

### 🎨 Animations & Visual Feedback
- [ ] **Splash Screen:** Automatic animated introduction upon launching the game with a double-click.
- [ ] **Menu Transitions:** Smooth animations triggered when navigating and pressing buttons in the main menus.
- [ ] **Smart Tutorial:** An input guide screen visible only during the player's very first game (skippable), which is automatically bypassed during quick post-death restarts.

## 📜 Credits & License

*   **Developed by**: Cipriano Salvatore / [minigame-tech](https://github.com/minigame-tech)
*   **Graphics Library (`g2d`)**: Michele Tomaiuolo

This project is licensed under the terms of the **MIT License**. Check the [`LICENSE`](LICENSE) file for more details.