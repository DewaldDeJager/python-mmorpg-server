### Entity System

The entity system is built on a hierarchical structure with the base `Entity` class providing core functionality for positioning, visibility, and serialization. This system is designed to handle everything from players and monsters to dropped items and map decorations.

#### Entity Hierarchy Diagram

The following ASCII diagram illustrates the inheritance structure of the entity system:

```text
       +------------------+
       |      Entity      | (Base class: x, y, instance, key, region)
       +------------------+
                |
    +-----------+-----------+----------------------+
    |                       |                      |
+-------+               +-------+             +---------+
|  NPC  |               |Character|           | Objects |
+-------+               +---------+           +---------+
                            |                      |
                +-----------+-----------+      +---+-------------------+-------------------+
                |                       |      |                       |                   |
            +--------+              +-------+  +-----------+       +-------+           +--------+
            | Player |              |  Mob  |  |   Item    |       | Chest |           |Resource|
            +--------+              +-------+  +-----------+       +-------+           +--------+
                                               | LootBag   |       | Effect|           | (Tree, |
                                               | Projectile|       +-------+           | Rock,  |
                                               +-----------+                           | etc.)  |
```

#### Key Components and Responsibilities

1.  **`Entity`**: The root class. Manages coordinates (`x`, `y`), unique instance IDs, and visibility logic (`isVisible`, `isNear`). It provides the basic `serialize` method used to send entity data to the client.
2.  **`Character`**: Extends `Entity`. Base class for sentient entities. Handles combat logic (`hit`, `heal`), status effects (poison, burning), and orientation. It introduces the concept of a `target` and `attackers`.
3.  **`Player`**: Extends `Character`. The most complex entity. Manages inventory, equipment, quests, skills, and networking (sending/receiving packets). It uses a `Handler` class to offload complex logic.
4.  **`Mob`**: Extends `Character`. Handles non-player characters that can engage in combat. Includes logic for drops, respawning, and roaming. It also uses a `Handler` for its AI and state management.
5.  **`NPC`**: Extends `Entity`. Simple non-combat entities used for dialogue and quest progression.
6.  **`Objects`**: Various subclasses of `Entity` representing non-character world elements:
    *   **`Item`**: Dropped items on the ground.
    *   **`Resource`**: Map elements like trees or rocks that can be harvested.
    *   **`Projectile`**: Entities that travel between characters to deliver hits.
    *   **`LootBag`**: Containers for multiple items dropped on death.

---

#### Entity Interaction Diagram

This diagram shows how entities interact with core game server systems:

```text
+-------------------+        +----------------------------------+
|      Network      | <----> |          World Manager           |
| (Packets/Sockets) |        | (State, Grids, Broadcaster)      |
+-------------------+        +----------------------------------+
          ^                           |                ^
          |                           v                |
          |                  +------------------+      |
          |                  |      Region      |      |
          |                  | (Area Tracking)  |      |
          |                  +------------------+      |
          |                           |                |
          |                           v                |
          |                  +------------------+      |
          +----------------- |      Entity      | -----+
                             +------------------+
                                      |
                 +--------------------+--------------------+
                 |                    |                    |
        +----------------+   +------------------+   +--------------+
        |    Database    |   |     Handlers     |   |    Combat    |
        | (Persistence)  |   | (Logic/Intervals)|   | (Hits/Status)|
        +----------------+   +------------------+   +--------------+
```

#### System Interactions Explained

*   **World Manager**: Acts as the central registry for all entities. It triggers the `tick()` loop and manages global state.
*   **Region System**: The world is divided into grids/regions. Entities are registered to regions, which optimizes visibility and packet broadcasting. When an entity moves, it updates its region, ensuring only nearby players receive its updates.
*   **Network Layer**: Entities (primarily `Player`) communicate with the client via packets. The `World` broadcasts entity state changes (movement, combat, spawning) to all players in the same or adjacent regions.
*   **Handlers**: Both `Player` and `Mob` utilize `Handler` classes. These handlers manage periodic updates (e.g., health regeneration, AI roaming) and process events like death or equipment changes, keeping the main entity classes cleaner.
*   **Database**: The `Player` entity interacts with the database to load and save progress (skills, inventory, location).
*   **Combat System**: `Character` entities interact with `Hit` and `StatusEffect` objects to process damage and buffs/debuffs. `Projectiles` are spawned to bridge the gap between an attacker and a target.
