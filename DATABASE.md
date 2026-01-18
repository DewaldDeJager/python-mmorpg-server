# Database Layer Documentation

This document describes the database layer of the Python Kaetram engine. The implementation is designed to be asynchronous, leveraging `motor` for MongoDB interactions and maintaining compatibility with the original TypeScript engine's structure.

## Overview

The database layer is responsible for persisting game state, user data, and world information. It follows a modular design where different components handle connection management, data loading, and entity creation.

### Component Diagram

The following ASCII diagram shows how the different components interact with each other:

```text
+---------------------------------------+
|                Main                   |
| (main.py)                             |
+-------------------+-------------------+
                    |
                    | 1. Initialize
                    v
+-------------------+-------------------+
|         DatabaseManager               |
| (database/database_manager.py)        |
+-------------------+-------------------+
                    |
                    | 2. Create Instance
                    v
+-------------------+-------------------+
|              MongoDB                  |
| (database/mongodb.py)                 |
+---------+---------+---------+---------+
          |         |         |
          |         |         | 3. Instantiate
          |         |         +-----------------------+
          |         |                                 |
          |         v                                 v
          |  +------+------+                   +------+------+
          |  |   Loader    |                   |   Creator   |
          |  | (loader.py) |                   | (creator.py)|
          |  +-------------+                   +-------------+
          |
          | 4. Async Connection (motor)
          v
+-------------------+-------------------+
|           MongoDB Server              |
+---------------------------------------+
```

## Core Components

### 1. DatabaseManager (`database/database_manager.py`)
A factory class that initializes the appropriate database engine based on the configuration. Currently, it exclusively supports MongoDB.
- **Purpose**: Decouples the application from the specific database implementation.
- **Key Method**: `get_database()` returns the active database instance.

### 2. MongoDB (`database/mongodb.py`)
The primary wrapper around the `motor` asynchronous MongoDB client.
- **Async Connection**: Uses `AsyncIOMotorClient` to handle non-blocking I/O.
- **Connection Verification**: Performs a `ping` command upon startup to ensure connectivity.
- **Callbacks**: Supports `on_ready` and `on_fail` hooks for the application to respond to connection state changes.
- **Reconnection Logic**: Managed in `main.py` via the `handle_fail` callback, which attempts to reconnect every 10 seconds.

### 3. Loader (`database/mongodb_loader.py`)
*Status: Stub*
Responsible for fetching data from the database. This will eventually handle loading player profiles, world state, and static game data.

### 4. Creator (`database/mongodb_creator.py`)
*Status: Stub*
Responsible for creating new records in the database, such as new player accounts or game events.

## Connection Flow

1.  **Initialization**: `Main` instantiates `DatabaseManager` during startup.
2.  **Configuration**: `DatabaseManager` reads connection details (host, port, credentials, TLS, SRV) from `common/config.py`.
3.  **Connection Attempt**: `Main` calls `database.create_connection()`.
4.  **Verification**: The `MongoDB` class attempts to ping the server.
    - **Success**: The `on_ready` callback is triggered, and `Main` proceeds to load the world.
    - **Failure**: The `on_fail` callback is triggered. If `SKIP_DATABASE` is false, the server enters a reconnection loop.

## Configuration

The database is configured via environment variables (or `.env` file) as defined in `common/config.py`:

- `DATABASE`: Type of database (e.g., `mongodb`).
- `SKIP_DATABASE`: If true, allows the server to run without a database connection.
- `MONGODB_HOST`: The hostname of the MongoDB server.
- `MONGODB_PORT`: The port number (default: 27017).
- `MONGODB_USER`/`MONGODB_PASSWORD`: Authentication credentials.
- `MONGODB_DATABASE`: The name of the database to use.
- `MONGODB_SRV`: Enable SRV connection string format.
- `MONGODB_TLS`: Enable TLS/SSL connection.

## Logging

The database layer uses structured logging from `common/log.py`.
- **INFO**: Connection attempts and status.
- **NOTICE**: Successful connection confirmation.
- **CRITICAL**: Connection failures and fatal errors.
