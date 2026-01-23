import time
from typing import Dict, Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from game.world import ConnectionCallback
from common.log import log
from network.connection import Connection
from network.modules import Constants

class AddressInfo:
    def __init__(self):
        self.count = 0
        self.last_time = 0

class SocketHandler:
    """
    This class acts as a central registry for all active connections.
    It tracks the number of connections per IP address to enforce limits.
    """

    def __init__(self):
        # Keeps track of addresses, their counts, and their last connection time.
        self.addresses: Dict[str, AddressInfo] = {}
        # List of all connections to the server, keyed by instance ID.
        self.connections: Dict[str, Connection] = {}
        
        self.connection_callback: Optional[ConnectionCallback] = None

    def add(self, connection: Connection):
        """
        Adds a connection to our dictionary of connections.
        """
        self.connections[connection.instance] = connection
        self.add_address(connection.address)
        
        if self.connection_callback:
            self.connection_callback(connection)

    def add_address(self, address: str):
        """
        Stores an address into our dictionary of addresses.
        """
        if address not in self.addresses:
            self.addresses[address] = AddressInfo()
            
        self.addresses[address].count += 1

    def remove(self, instance: str):
        """
        Used to remove connections from our dictionary of connections.
        """
        if instance not in self.connections:
            return
            
        connection = self.connections[instance]
        self.remove_address(connection.address)
        
        del self.connections[instance]

    def remove_address(self, address: str):
        """
        Removes an address from our dictionary.
        """
        if address not in self.addresses:
            return
            
        self.addresses[address].count -= 1
        
        if self.addresses[address].count <= 0:
            del self.addresses[address]

    def get(self, instance: str) -> Optional[Connection]:
        """
        Finds and returns a connection in our dictionary of connections.
        """
        return self.connections.get(instance)

    def is_max_connections(self, address: str) -> bool:
        """
        Checks whether the current IP address has reached the maximum allowed connections.
        """
        if address not in self.addresses:
            return False
        return self.addresses[address].count > Constants.MAX_CONNECTIONS

    def has_connections(self) -> bool:
        """
        Checks whether or not we have anyone currently connected to the server.
        """
        return len(self.connections) > 0

    def update_last_time(self, address: str):
        """
        Updates the last time a connection was made from an address.
        """
        if address not in self.addresses:
            self.addresses[address] = AddressInfo()
        self.addresses[address].last_time = int(time.time() * 1000)

    def on_connection(self, callback: ConnectionCallback):
        """
        The callback for when a new connection is received.
        """
        self.connection_callback = callback
