# Python Server Network Layer Documentation

The networking layer in the Python implementation of Kaetram is designed for asynchronous performance using **FastAPI** and **WebSockets**. It mirrors the structure of the original TypeScript implementation while adapting to Pythonic idioms and the FastAPI framework.

## 1. Low-Level Socket Management (`main.py`)

The server uses **FastAPI**'s WebSocket support to handle incoming connections.

- **FastAPI WebSocket Endpoint**: The `/ws` endpoint in `main.py` accepts incoming WebSocket connections.
- **Connection Lifecycle**: For each new connection:
    1. A unique `instance_id` (format: `{{type}}-{{id}}`) is generated.
    2. A `Connection` wrapper is created for the `WebSocket` object.
    3. The connection is registered with the `SocketHandler`.
    4. Registration triggers the `on_connection` callback in `Main`, which validates server status and world capacity.
    5. If valid, `Main` calls `World.connection_callback`, which defaults to `NetworkManager.handle_connection`.
    6. `NetworkManager` performs final checks (bans, rate limits) and instantiates the `Player`.
    7. A message loop is started in `main.py` to receive and process messages from the client.

## 2. Connection Wrapper (`network/connection.py`)

The `Connection` class wraps the raw FastAPI `WebSocket` to add safety, utility features, and state management.

- **Responsibility**: Acts as the bridge between the raw socket and the game logic.
- **Rate Limiting**: Tracks message rates and provides a mechanism to disconnect clients that exceed limits.
- **Duplicate Filtering**: Filters out duplicate messages received within a short threshold (100ms) to prevent accidental spam or client-side issues.
- **Timeouts**: Manages idle timeouts and asynchronous heartbeats (pings) to ensure the connection is still alive.
- **Sending Data**: Provides methods (`send`, `send_utf8`) to send data back to the client, handling JSON serialization.

## 3. Socket Handler (`network/socket_handler.py`)

This class acts as a central registry for all active connections.

- **Tracking**: Maintains a dictionary of active `Connection` objects, keyed by their unique `instance` ID.
- **Address Limits**: Tracks the number of connections per IP address (`AddressInfo`) to prevent multi-accounting or DDoS attempts (`is_max_connections`).
- **Lifecycle Hooks**: Provides callbacks for when a connection is added or removed.

## 4. High-Level Network Manager (`network/network_manager.py`)

The `NetworkManager` class resides in the game logic layer and orchestrates communication between the game world and the networking infrastructure.

- **Packet Queueing**: Maintains a queue of outgoing packets for each player instance.
- **Flushing**: The `parse()` method (called by the game loop) flushes these queues, sending all pending packets to their respective clients in a single batch.
- **Connection Handling**: When a connection is accepted, it:
    - Checks if the IP is banned in the database.
    - Enforces rate limits on connection attempts (time between logins).
    - Enforces maximum connections per IP.
    - Prepares the state for the `Player` entity (to be implemented).
- **Broadcasting**: Provides helper methods to send packets to:
    - Specific Players (`send`)
    - List of Players (`send_to_players`)
    - Entire Map Regions (`send_to_region`, `send_to_surrounding_regions`)
    - All Players (`broadcast`)

## Architecture Diagram

```text
+------------------+         +-----------------------+
|     Client       |         |       Main App        |
| (Web Browser/JS) |         | (FastAPI /ws endpoint)|
+--------+---------+         +-----------+-----------+
         |                               |
         |         WebSocket             |
         +-----------------------------> |
                                         | 1. Creates
                                         v
                                 +-------------------+
                                 |    Connection     |
                                 | (WebSocket Wrapper)|
                                 +---------+---------+
                                         |
                       +-----------------+-----------------+
                       |                                   |
                2. Registers                        3. Handles
                       v                                   v
             +-------------------+               +-------------------+
             |   SocketHandler   |               |  NetworkManager   |
             | (Registry/Limits) | <-----------+ |  (Game Interface) |
             +-------------------+               +---------+---------+
                                                           |
                                                    4. Queues/Flushes
                                                           v
                                                 +-------------------+
                                                 |   Packet Queues   |
                                                 |  (Per Instance)   |
                                                 +-------------------+
```

## Summary Flow

1. **Client Connects**: The client initiates a WebSocket connection to the `/ws` endpoint in `main.py`.
2. **Connection Creation**: FastAPI accepts the connection, and a `Connection` wrapper is created with a unique `instance_id`.
3. **Registration**: The `Connection` is added to `SocketHandler`, which triggers its `on_connection` callback.
4. **Main Validation**: `Main.handle_connection` (the registered callback) performs initial server-level checks:
    - Is the server ready?
    - Are connections allowed in the world?
    - Is the world full?
5. **World Handover**: If valid, `Main` calls `World.connection_callback`.
6. **Network Manager Validation**: `World.connection_callback` (pointing to `NetworkManager.handle_connection`) performs final networking checks:
    - Is the IP banned?
    - Is the connection attempt too fast (rate limiting)?
    - Has the IP reached maximum allowed connections?
7. **Player Instantiation**: If all checks pass, the `Player` object is instantiated, the `ConnectedPacket` is sent, and the message loop begins.
