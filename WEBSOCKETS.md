# WebSocket Protocol Documentation

This document describes the WebSocket communication protocol used between the game client and server.

## 1. Overview

The communication is based on asynchronous WebSockets, transferring JSON-encoded messages. To optimize performance, the server and client support message batching.

## 2. Message Format

Messages are sent as JSON arrays. A single message or a batch of messages can be sent in a single WebSocket frame.

### 2.1. Packet Structure

Each packet follows a specific positional format in a JSON array:

`[PacketID, (Opcode), Data, (BufferSize)]`

- **PacketID** (Required): An integer representing the packet type (see [Packets](#4-packets)).
- **Opcode** (Optional): An integer representing a sub-type or action for the specific PacketID.
- **Data** (Required/Optional): The payload of the packet. Can be a primitive (string, number), a dictionary (object), or omitted depending on the packet.
- **BufferSize** (Optional): Used in some packets to indicate expected data length.

### 2.2. Batching

Multiple packets can be sent together in a single JSON array:

`[[Packet1], [Packet2], [Packet3]]`

The client and server should both be able to handle receiving a single packet array or an array of packet arrays.

## 3. Connection Flow

The initial handshake and login process follow a strict sequence of packets:

1.  **Connected** (Server -> Client):
    - Sent immediately after the WebSocket connection is established.
    - Signal to the client that the server is ready to receive the handshake.
2.  **Handshake** (Client -> Server):
    - The client sends its identification (type, version, etc.).
3.  **Handshake** (Server -> Client):
    - The server responds with confirmation and potentially server time/instance details.
4.  **Login** (Client -> Server):
    - The client sends credentials (username, password/guest).
5.  **Welcome** (Server -> Client):
    - Sent if login is successful. Contains player's initial state.
6.  **Map** (Server -> Client):
    - Sent to provide the map data for the player's location.
7.  **Ready** (Client -> Server):
    - The client sends this once it has loaded the map and is ready to start receiving entity updates.

## 4. Packets

### 4.1. Connected (ID: 0)
**Direction**: Server -> Client
**Payload**: None
**Format**: `[0, null]` or `[0]`

### 4.2. Handshake (ID: 1)
**Direction**: Bidirectional

**Client -> Server**:
```json
[1, {
  "type": "client",
  "version": "1.0.0"
}]
```

**Server -> Client**:
```json
[1, {
  "type": "client",
  "serverTime": 1700000000000,
  "instance": "player-unique-id"
}]
```

### 4.3. Login (ID: 2)
**Direction**: Client -> Server
**Opcodes**:
- `Login`: 0
- `Register`: 1
- `Guest`: 2

**Format**: `[2, Opcode, Data]`

**Example (Guest Login)**:
```json
[2, 2, {
  "username": "Guest123"
}]
```

### 4.4. Ready (ID: 11)
**Direction**: Client -> Server
**Format**: `[11, { "regionsLoaded": 1, "userAgent": "..." }]`

*Note: Packet IDs may vary based on the `Packets` enum implementation.*

## 5. Heartbeat

The server uses a 30-second verification interval to ensure connections are alive. Clients should respond to server-side pings or maintain activity to avoid being timed out (default 10 minutes).
