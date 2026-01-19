# Project Guidelines

This project is a Python implementation of an MMORPG game server, inspired by the Kaetram game engine written in
TypeScript.

## General Guidelines

1. **Minimize Dependencies**: We strive to keep the project lightweight and maintainable by avoiding unnecessary
   third-party libraries. We prefer standard library solutions or robust, minimal foundational libraries over heavy,
   opinionated frameworks.
    - **FastAPI**: Used for the networking layer and WebSocket support.
    - **Pydantic V2**: Used for data validation and serialization (Packets, Models).
    - **Motor**: Used as the asynchronous MongoDB driver.
2. **Pure Python**: The goal is to leverage Python's strengths and keep the codebase "Pythonic".
    - Use **type hints** (PEP 484) throughout the codebase to ensure type safety and better IDE support.
    - Follow **PEP 8** for code style and formatting.
    - Use **type aliases** for complex types, such as callbacks, to improve readability (e.g., `MovementCallback = Callable[[int, int], None]`).
    - Prefer **Python datetime types** (`datetime`, `timedelta`) where time calculations or similar logic are used, ensuring idiomatic time handling.
    - Prefer asynchronous programming (`async`/`await`) for I/O bound operations.
3. Any comments from the original implementation should be retained as there are many comments that are beneficial in
   understanding the logic
4. **Testing**: Use `pytest` for unit and integration tests. Tests should be located in the `tests/` directory.
5. **Serialization**: Use `CamelModel` (a Pydantic wrapper) for models that interact with the client to maintain
   compatibility with the original camelCase naming convention.
6. **Logic**: Match the original logic and structure where possible, including file and directory names where
   appropriate. Suggest a different implementation if it makes more sense in idiomatic Python or if there is an obvious
   enhancement that can be made.
7. **Project Structure**: The project structure is documented in the `PROJECT_STRUCTURE.md` file at the root of the project.
8. **Documentation**: Update the relevant documentation files whenever a key change is made so that the documentation is kept up to date. Key documentation files include:
   - README.md
   - PROJECT_STRUCTURE.md
   - DATABASE.md
   - NETWORK.md
   - ENTITY.md
9. **Kaetram**: The source code for the original Kaetram project is located in the `/Kaetram-Open` directory.

