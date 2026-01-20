from network.socket_handler import SocketHandler
from database.database_manager import Database

class World:
    """
    A stub World class to satisfy the Character dependency.
    """
    def __init__(self, socket_handler: SocketHandler, database: Database):
        self.socket_handler = socket_handler
        self.database = database
