# Multiplayer Snake Game

Welcome to the Multiplayer Snake Game! 🎮🐍

This project is a fun and interactive multiplayer version of the classic Snake game. It lets you and your friends compete in real-time to see who can grow their snake the longest. Built with Python and Pygame for the client-side, and WebSockets for the server-side communication.

## Features

- **Multiplayer Support**: Play against friends in real-time.
- **Dynamic Gameplay**: Eat fruit to grow your snake and score points.
- **Collision Detection**: Crashing into other snakes or the walls has real consequences.
- **Simple Mechanics**: Easy to pick up and play, with classic Snake game rules.

## Getting Started

To get started with the game, follow these steps:

### Prerequisites

- Python 3.8 or higher
- Pygame
- WebSockets library

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Oussamabh242/snake-multiplayer.git
    cd snake-multiplayer
    ```

2. **Install dependencies:**

    You will need to install the required Python libraries. You can do this using pip:

    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Server:**

    Start the WebSocket server with:

    ```bash
    python3 server.py
    ```

4. **Run the Game:**

    Start the game client with:

    ```bash
    python3 main.py
    ```

5. **Connect and Play:**

    Follow the prompts to create or join a room, and start playing!

## Usage

- **W** to move up
- **S** to move down
- **A** to move left
- **D** to move right

The game will automatically handle collisions, growth, and scoring. I

## Contributing

If you want to contribute to this project, feel free to open an issue or submit a pull request. Any improvements or bug fixes are welcome!
