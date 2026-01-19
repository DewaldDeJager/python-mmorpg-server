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
- [x] **Connection Handler**: Created `network/connection.py` (equivalent of `Connection.ts`) that:
    - [x] Wraps the raw websocket.
    - [x] Handles message decoding (JSON parsing).
    - [x] Routes messages based on `Opcode` (implemented via `message_callback`).
    - [x] Manages rate limiting and packet queuing.

## 3. Database Layer
- [x] **Database Strategy**: Selected **Raw Motor + Pydantic** to minimize dependencies and match the TS architecture.
- [x] **Driver**: Using `motor` (AsyncIO driver for MongoDB).
- [ ] **Database Loader**: Implement `database/mongodb_loader.py`.
    - [ ] Authentication logic (verifying credentials).
    - [ ] Loading player data (stats, inventory, equipment).
    - [ ] Loading world and social data (guilds, bans).
- [ ] **Database Creator**: Implement `database/mongodb_creator.py`.
    - [ ] New player account creation.
    - [ ] Saving player progress and state.
- [x] **Models**: Port the TypeScript interfaces (e.g., `PlayerInfo`) from `@kaetram/common/database` to raw Pydantic models.

## 4. World Manager & Game Loop
The `World` class is the central hub of the server, orchestrating all systems.
- [ ] **World Orchestration**: Implement `game/world.py` to initialize and link core systems:
    - [ ] **Map & Region System**: Link the world to the map and its grid-based regions.
    - [ ] **Entity Registry**: Manage all active `Players`, `Mobs`, and `NPCs`.
    - [ ] **Network Integration**: Link to `NetworkManager` for packet handling.
- [ ] **The Game Tick**: Implement the main server loop using `asyncio`:
    - [ ] **Network Parse**: Process incoming packets from all connections.
    - [ ] **Region Updates**: Trigger visibility logic and state synchronization for each region.
    - [ ] **Persistence Loop**: Implement periodic saving of player data to the database.
- [ ] **Packet Distribution**: Implement the `push` mechanism for targeted broadcasting:
    - [ ] **Direct Messaging**: Sending packets to individual players.
    - [ ] **Region-based Broadcast**: Sending packets to players in a specific region or surrounding regions.
    - [ ] **Global Broadcast**: Server-wide announcements and updates.
- [ ] **World State & Utilities**:
    - [ ] Population tracking and capacity management.
    - [ ] Global configuration overrides (e.g., experience rates, drop probabilities).
    - [ ] Helper methods for finding entities by name or ID.

## 5. Entity System & Logic
Implement entities one at a time, following the hierarchy:
- [ ] **Base Entity**: Implement `Entity` class (`game/entity/entity.py`).
    - Position (x, y), Instance ID, visibility logic.
    - Integration with `World` and `Region`.
- [ ] **Character Base**: Implement `Character` class (`game/entity/character.py`).
    - Combat stats (HP, MaxHP), movement state.
    - Combat logic (hit, heal, status effects).
- [ ] **Player Entity**: Implement `Player` class (`game/entity/character/player.py`).
    - Handshake and Login flow.
    - Database integration (loading/saving state).
    - Inventory, Equipment, Skills, and Quests.
    - Packet handling and routing.
- [ ] **Mob Entity**: Implement `Mob` class (`game/entity/character/mob.py`).
    - AI behavior (roaming, aggro).
    - Drop tables and respawn logic.
- [ ] **NPC Entity**: Implement `NPC` class (`game/entity/npc.py`).
    - Dialogue and quest triggers.
- [ ] **Item & Object Entities**:
    - `Item` (dropped loot), `Chest`, `Resource` (trees/rocks).
- [ ] **Movement Logic**: Port movement validation and pathing logic.
- [ ] **Login Flow**: Complete the "Handshake" -> "Login" -> "Database Load" -> "Spawn" flow.
