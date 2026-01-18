import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager

from common.config import config
from common.log import log
from database.database_manager import Database

class Main:
    def __init__(self):
        self.database = Database(config.database).get_database()
        self.ready = False

        if self.database:
            self.database.on_ready(self.handle_ready)
            self.database.on_fail(self.handle_fail)

    async def start(self):
        if not self.handle_licensing():
            return

        log.info(f"Initializing {config.name} game engine...")

        if self.database:
            await self.database.create_connection()
        else:
            self.handle_ready(without_database=True)

    def handle_ready(self, without_database: bool = False):
        self.ready = True

        # self.load_world() # To be implemented later

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.host, port=config.port)
