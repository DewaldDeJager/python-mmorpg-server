# Python MMORPG Server

This is a Python-based MMORPG server implementation. The initial implementation is based on
by [Kaetram](https://github.com/Kaetram/Kaetram-Open) which is a fork of
the [BrowserQuest](https://github.com/mozilla/BrowserQuest) project.

## Guiding Principles

1. **Minimize Dependencies**: We strive to keep the project lightweight and maintainable by avoiding unnecessary
   third-party libraries. We prefer standard library solutions or robust, minimal foundational libraries (like
   `pydantic`, `motor`, `fastapi`) over heavy, opinionated frameworks when possible.
2. **Pure Python**: The goal is to leverage Python's strengths and keep the codebase "Pythonic". We avoid complex
   abstractions that hide the underlying logic unless they provide significant safety or productivity benefits without
   compromising performance or transparency.

## Documentation

For more detailed information about specific subsystems, refer to the following documentation files:

- [**PROJECT_STRUCTURE.md**](PROJECT_STRUCTURE.md): An overview of the directory structure and the purpose of each
  component.
- [**DATABASE.md**](DATABASE.md): Detailed documentation of the database layer, including component diagrams and
  connection flows.
- [**NETWORK.md**](NETWORK.md): Information about the network layer, WebSocket management, and the `NetworkManager`.
- [**ENTITY.md**](ENTITY.md): Documentation of the entity system, hierarchy, and interactions between game entities.
- [**ROADMAP.md**](ROADMAP.md): Project goals, completed tasks, and planned features.

## Development

### Type Checking

We use `mypy` for static type checking. To run the type checker:

```bash
uv run mypy .
```

Configuration can be found in `pyproject.toml`.

## Decision Log

| Decision                                 | Date       | Rationale                                                                                                                                                                                                                                            | Alternatives / Drawbacks                                                                                                                                                                                                                                     |
|:-----------------------------------------|:-----------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Serialization: Pydantic V2**           | 2026-01-14 | Chosen for its speed (Rust-core) and robustness in defining complex nested structures (Packets).                                                                                                                                                     | **Alternative:** `dataclasses` (less features), `marshmallow` (slower).                                                                                                                                                                                      |
| **Networking: FastAPI**                  | 2026-01-15 | Chosen for its high performance (Starlette-based), built-in WebSocket support, and excellent integration with Pydantic for data validation.                                                                                                          | **Alternative:** `websockets` library (too low level), `Django` (too heavy).                                                                                                                                                                                 |
| **Database Layer: Raw Motor + Pydantic** | 2026-01-16 | Chosen to strictly adhere to the "minimize dependencies" principle and maintain architectural parity with the TypeScript server (which uses the native MongoDB driver). It offers the best performance and explicit control over data serialization. | **Alternative:** Beanie (ODM).<br>**Drawbacks:** Beanie adds an extra dependency layer and abstraction overhead. While it offers a better developer experience with less boilerplate, it diverges from the TS implementation and adds weight to the project. |
| **Dependency Injection: Explicit Instantiation** | 2026-01-19 | Core game logic and engine services (Main, NetworkManager, SocketHandler) are explicitly instantiated to maintain total control over state, performance, and initialization order. This avoids the mismatch between request-based lifecycles and the persistent nature of a game server. | **Alternative:** FastAPI `Depends()`. <br>**Drawbacks:** `Depends()` adds overhead, complicates state management for singletons, and creates tight coupling with FastAPI. It also doesn't work outside of routes (e.g., in background tasks or game loops). |
| **Static Type Checking: Mypy**           | 2026-01-21 | Added to improve code reliability, catch common errors early, and serve as live documentation of the codebase's types.                                                                                                                              | **Alternative:** Pyright. <br>**Drawbacks:** Initial setup requires resolving various type inconsistencies and adding annotations.                                                                                                                           |
