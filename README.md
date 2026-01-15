# Python MMORPG Server

This is a Python-based MMORPG server implementation based on Kaetram.

## Guiding Principles

1.  **Minimize Dependencies**: We strive to keep the project lightweight and maintainable by avoiding unnecessary third-party libraries. We prefer standard library solutions or robust, minimal foundational libraries (like `pydantic`, `motor`, `fastapi`) over heavy, opinionated frameworks when possible.
2.  **Pure Python**: The goal is to leverage Python's strengths and keep the codebase "Pythonic". We avoid complex abstractions that hide the underlying logic unless they provide significant safety or productivity benefits without compromising performance or transparency.
3.  **Parity with TypeScript**: While idiomatic Python is preferred, the architecture should closely follow the reference TypeScript implementation to ensure compatibility and ease of migration.

## Decision Log

| Decision | Date | Rationale | Alternatives / Drawbacks |
| :--- | :--- | :--- | :--- |
| **Database Layer: Raw Motor + Pydantic** | 2026-01-16 | Chosen to strictly adhere to the "minimize dependencies" principle and maintain architectural parity with the TypeScript server (which uses the native MongoDB driver). It offers the best performance and explicit control over data serialization. | **Alternative:** Beanie (ODM).<br>**Drawbacks:** Beanie adds an extra dependency layer and abstraction overhead. While it offers a better developer experience with less boilerplate, it diverges from the TS implementation and adds weight to the project. |
| **Networking: FastAPI** | 2026-01-15 | Chosen for its high performance (Starlette-based), built-in WebSocket support, and excellent integration with Pydantic for data validation. | **Alternative:** `websockets` library (too low level), `Django` (too heavy). |
| **Serialization: Pydantic V2** | 2026-01-14 | Chosen for its speed (Rust-core) and robustness in defining complex nested structures (Packets). | **Alternative:** `dataclasses` (less features), `marshmallow` (slower). |
