import asyncio
from typing import Optional, Callable, Any
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from common.log import log
from database.mongodb_loader import Loader
from database.mongodb_creator import Creator

class MongoDB:
    """
    MongoDB connection manager that handles the asynchronous connection to the database.
    It initializes the Loader and Creator classes upon a successful connection.
    """
    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        database_name: str,
        tls: bool,
        srv: bool,
        auth_source: str
    ):
        srv_insert = "mongodb+srv" if srv else "mongodb"
        auth_insert = f"{username}:{password}@" if username and password else ""
        port_insert = f":{port}" if port > 0 and not srv else ""
        auth_source_insert = f"?authSource={auth_source}" if auth_source else ""
        
        self.connection_url = f"{srv_insert}://{auth_insert}{host}{port_insert}/{database_name}{auth_source_insert}"
        self.database_name = database_name
        self.tls = tls
        
        self.database: Optional[AsyncIOMotorDatabase] = None
        self.loader: Optional[Loader] = None
        self.creator: Optional[Creator] = None
        
        self.ready_callback: Optional[Callable[[], Any]] = None
        self.fail_callback: Optional[Callable[[Exception], Any]] = None

    async def create_connection(self) -> None:
        """
        Attempts to connect to MongoDB. Times out after 5 seconds if
        no MongoDB server is present for the given host.
        """
        try:
            client: AsyncIOMotorClient = AsyncIOMotorClient(
                self.connection_url,
                connectTimeoutMS=5000,
                serverSelectionTimeoutMS=5000,
                tls=self.tls
            )
            
            # The client doesn't actually connect until we do something
            # Trigger a command to check connection
            await client.admin.command('ping')
            
            self.database = client[self.database_name]
            self.loader = Loader(self.database)
            self.creator = Creator(self.database)
            
            log.notice("Successfully connected to the MongoDB server.")
            
            if self.ready_callback:
                if asyncio.iscoroutinefunction(self.ready_callback):
                    await self.ready_callback()
                else:
                    self.ready_callback()
                    
        except Exception as e:
            self.loader = Loader(None)
            
            if self.fail_callback:
                if asyncio.iscoroutinefunction(self.fail_callback):
                    await self.fail_callback(e)
                else:
                    self.fail_callback(e)
            else:
                log.critical(f"Could not connect to the MongoDB server: {e}")

    def on_ready(self, callback):
        self.ready_callback = callback

    def on_fail(self, callback):
        self.fail_callback = callback

    async def is_ip_banned(self, ip: str) -> bool:
        """
        Checks whether or not an IP string is contained within the database collection
        for IP bans.

        :param ip: The IP string that we are checking for.
        :return: True if the IP is banned, False otherwise.
        """
        # TODO: Implement database query for IP bans
        # cursor = self.database.ipbans.find({"ip": ip})
        # return await cursor.to_list(length=1) is not None
        return False
