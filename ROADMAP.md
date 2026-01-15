# Python Server Rebuild Roadmap

This document outlines the steps to rebuild the Kaetram server in Python.

## 1. Complete Networking Data Structures
- [x] **Core Packet Infrastructure**: `Packet` class, `CamelModel`, and enum conversions.
- [x] **Initial Packets**: `Handshake`, `Movement`, `Combat`, `Chat`, `Container`, etc.
- [x] **Expanded Packets**: `Entity`, `World`, `Items`, `Inventory`, `Social`, `Guilds`, `UI`, `System`, `Game Logic`.
- [x] **Finish Remaining Packets**: Implement the remaining ~15 packets (e.g., `Quest`, `Trade`, `Shop`, `Movement` refinement).
- [x] **Protocol Verification**: Created a comprehensive unit test suite (`tests/test_packets.py`) using `pytest` that serializes **all 52 implemented packet types** and ensures 100% compatibility with the TypeScript protocol.

## 2. Core Networking Engine (The "Socket" Layer)
This is the bridge between your Pydantic packets and the network.
- [x] **Technology Choice**: Use **FastAPI** (with `uvicorn`) to handle both HTTP and WebSocket connections.
- [ ] **Connection Handler**: Create a Python equivalent of `Connection.ts` that:
    - Wraps the raw websocket.
    - Handles message decoding (JSON parsing).
    - Routes messages based on `Opcode` to the correct handler.
    - Manages rate limiting and packet queuing.

## 3. Database Layer
- [x] **Database Strategy**: Selected **Raw Motor + Pydantic** to minimize dependencies and match the TS architecture.
- [ ] **Driver**: Use `motor` (AsyncIO driver for MongoDB) to prevent blocking the game loop.
- [x] **Models**: Port the TypeScript interfaces (e.g., `PlayerInfo`) from `@kaetram/common/database` to raw Pydantic models.

## 4. The Game Loop
- [ ] **Main Loop**: Implement a specialized `asyncio` loop that ticks 60 times per second (or your target tick rate).
- [ ] **World Manager**: Create the `World` class to hold the state of all `Players`, `Mobs`, and `Regions`.
- [ ] **Region System**: Implement the grid/region logic to optimize collision detection and packet broadcasting (only sending updates to nearby players).

## 5. Entity System & Logic
- [ ] **Entity Class**: Create the base `Entity` class and subclasses (`Player`, `Mob`, `NPC`).
- [ ] **Movement Logic**: Port the movement validation and pathing logic.
- [ ] **Login Flow**: Connect the "Handshake" -> "Login" -> "Database Load" -> "Spawn" flow.
