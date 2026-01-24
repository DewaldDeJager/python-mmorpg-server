import asyncio
import json
from fastapi import FastAPI
from contextlib import asynccontextmanager

from common.config import config
from common.log import log
from database.database_manager import Database
from game.world import World
from network.socket_handler import SocketHandler
from network.connection import Connection
from network.modules import EntityType
from common.utils import utils
from game.info.loader import Loader
from fastapi import WebSocket, WebSocketDisconnect


class Main:
    def __init__(self):
        self.world = None
        self.database = Database(config.database).get_database()
        self.ready = False
        self.socket_handler = SocketHandler()

        self.socket_handler.on_connection(self.handle_connection)

        if self.database:
            self.database.on_ready(self.handle_ready)
            self.database.on_fail(self.handle_fail)

    async def handle_connection(self, connection: Connection):
        """
        We handle each new connection here. We check if the world is full,
        and if there is room, we make a callback in the world to handle the rest.
        @param connection The new connection we received from the WebSocket.
        """
        if not self.ready or not self.world or not self.world.allow_connections:
            await connection.reject('disallowed')
            return

        if self.world.is_full():
            log.notice("The world is currently full, connections are being rejected.")
            await connection.reject('worldfull')
            return

        if self.world.connection_callback:
            log.debug(f"Handling connection with callback for {connection.instance}.")
            await self.world.connection_callback(connection)

    async def start(self):
        if not self.handle_licensing():
            return

        log.info(f"Initializing {config.name} game engine...")

        if self.database:
            await self.database.create_connection()
        else:
            self.handle_ready(without_database=True)

        Loader()

    def handle_ready(self, without_database: bool = False):
        self.ready = True

        log.info(f"************** {config.name} World **************")
        self.world = World(self.socket_handler, self.database)

        if without_database:
            log.notice("Running without database - Server is now accepting connections.")

        log.notice(f"Server is now listening on port: {config.port}.")

    async def handle_fail(self, error: Exception):
        if config.skip_database:
            return self.handle_ready(without_database=True)

        log.critical("Could not connect to the MongoDB server.")
        log.critical(f"Error: {error}")

        log.info("Attempting to reconnect in 10 seconds...")

        await asyncio.sleep(10)
        if self.database:
            await self.database.create_connection()

    def handle_licensing(self) -> bool:
        if not config.accept_license:
            log.critical(
                "You must read and accept both MPL2.0 and OPL licensing agreements. "
                "Once you've done so, toggle ACCEPT_LICENSE in your environment variables."
            )
            return False
        return True

main_instance = Main()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    log.debug("Starting game engine...")
    await main_instance.start()
    yield
    # Shutdown logic (e.g., saving players)
    log.info("Shutting down game engine.")


app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": f"Python {config.name} Server"}


@app.get("/health")
async def health_check():
    return {"status": "ok", "ready": main_instance.ready}


@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    # Create a unique instance ID for this connection
    instance_id = utils.create_instance(EntityType.Player)
    connection = Connection(instance_id, websocket)

    # Register the connection in the socket handler
    # This will trigger Main.handle_connection via the on_connection callback
    await main_instance.socket_handler.add(connection)

    try:
        while not connection.closed:
            # Wait for messages from the client
            data = await websocket.receive_text()

            # Rate limiting check
            connection.message_rate += 1
            if connection.message_rate > 50:  # Example limit
                await connection.reject("spam")
                break

            # Duplicate check
            if connection.is_duplicate(data):
                continue

            # Refresh timeout on activity
            connection.refresh_timeout()

            # Parse the message (typically JSON)
            try:
                message = json.loads(data)
                if connection.message_callback:
                    await connection.message_callback(message)
                else:
                    # Fallback if no callback is registered yet (e.g. before Player is created)
                    log.debug(f"Received message from {connection.address} without callback: {message}")
            except json.JSONDecodeError:
                log.warning(f"Received non-JSON message from {connection.address}: {data}")

    except WebSocketDisconnect:
        await connection.handle_close()
    except Exception as e:
        log.error(f"WebSocket error for {connection.address}: {e}")
        await connection.handle_close(str(e))
    finally:
        main_instance.socket_handler.remove(instance_id)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=config.host, port=config.port, reload=config.debugging)
