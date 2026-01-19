# Project Structure

This document provides an overview of the directory structure and the purpose of each component in the Kaetram Python MMORPG server.

## Root Directory

- `main.py`: The entry point of the application. Initializes the FastAPI server and game components.
- `pyproject.toml`: Configuration for the Python project, including dependencies and tool settings (used by `uv`).
- `Dockerfile` & `docker-compose.yml`: Configuration for containerizing the application and its dependencies (like MongoDB).
- `README.md`: General project overview and setup instructions.
- `DATABASE.md`, `ENTITY.md`, `NETWORK.md`: Specialized documentation for specific subsystems.
- `ROADMAP.md`: Project goals and planned features.
- `Kaetram-Open/`: The original TypeScript implementation of Kaetram, used as a reference for logic and structure.

## Core Directories

### `common/`
Contains shared utility modules used across the entire project.
- `config.py`: Application configuration management.
- `log.py`: Centralized logging setup.

### `database/`
Handles all interactions with the MongoDB database.
- `database_manager.py`: Orchestrates database operations.
- `mongodb.py`: Low-level MongoDB connection and client setup using `Motor`.
- `mongodb_loader.py` & `mongodb_creator.py`: Logic for loading existing data and creating new database entries.
- `models/`: Pydantic models (using `CamelModel`) representing database schemas for `player`, `guild`, `statistics`, etc.

### `game/`
Contains the core game engine logic, state management, and entity systems.
- `entity/`: Defines the base `Entity` class and specialized sub-entities.
    - `character/`: Base classes for characters (mobile entities).
        - `combat/`: Combat system logic (e.g., `Hit`).
        - `player/`: Logic specific to player entities.
    - `npc/`: Logic for Non-Player Characters (mobs, vendors).
    - `objects/`: Logic for static or interactable world objects (resources, etc.).

### `network/`
Manages real-time networking, WebSocket connections, and the packet protocol.
- `network_manager.py`: Manages active connections and packet routing.
- `socket_handler.py`: Handles raw WebSocket events.
- `packet.py` & `packets.py`: Base packet definitions and serialization logic.
- `opcodes.py`: Mapping of packet types to their numeric identifiers.
- `shared_types.py`: Type definitions used in networking models.
- `impl/`: Concrete implementations of various packet types (e.g., `chat.py`, `movement.py`, `combat.py`), mirroring the client-server protocol.

### `tests/`
Contains the automated test suite.
- `test_packets.py`: Unit tests for packet serialization and validation.
- `test_ws.py`: Integration tests for WebSocket communication.

### `logs/`
Directory for storing application log files.
