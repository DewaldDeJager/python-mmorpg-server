import time
from typing import Dict, List, Any, Optional
from common.config import config
from common.log import log
from network.connection import Connection
from network.socket_handler import SocketHandler

class NetworkManager:
    """
    The NetworkManager class sits in the Game Logic layer and orchestrates 
    communication between the World and the SocketHandler.
    """

    def __init__(self, database, socket_handler: SocketHandler):
        self.database = database
        self.socket_handler = socket_handler
        
        # In the original, world.map.regions is used. 
        # For now, we'll leave it as None until World/Regions are implemented.
        self.regions = None
        
        self.timeout_threshold = 5000 # 5 seconds
        self.packets: Dict[str, List[Any]] = {}

    async def parse(self):
        """
        This function parses all the packets currently in the queue.
        We take each player instance and for each one we parse its
        outstanding packets. Those are sent to each player's connection.
        When we're done, we remove the packet from the queue.
        """
        # Create a list of keys to iterate over to avoid "dictionary changed size during iteration"
        instances = list(self.packets.keys())
        
        for instance in instances:
            queue = self.packets.get(instance)
            if queue and len(queue) > 0:
                connection = self.socket_handler.get(instance)
                
                if connection:
                    await connection.send(queue)
                    self.packets[instance] = []
                else:
                    self.socket_handler.remove(instance)

    async def handle_connection(self, connection: Connection):
        """
        We create a player instance when we receive a connection and begin a
        handshake with the client.
        """
        # In original, it checks if IP is banned.
        # Since database logic might be complex and not fully known, 
        # we'll assume a simple check or a TODO if not available.
        
        is_banned = False
        if hasattr(self.database, 'is_ip_banned'):
            # This is likely async in our Python implementation
            is_banned = await self.database.is_ip_banned(connection.address)
        
        if is_banned:
            await connection.reject('banned')
            return

        # Create the packet queue for the connection instance.
        self.packets[connection.instance] = []

        # Check the time difference between the last connection.
        last_time = self.get_last_connection(connection)
        time_difference = (time.time() * 1000) - last_time

        # Update the last time the connection was made.
        self.socket_handler.update_last_time(connection.address)

        # Skip if we are in debug mode.
        if not config.debugging:
            # Check that the connections aren't coming too fast.
            if time_difference < self.timeout_threshold:
                await connection.reject('toofast')
                return

            # Ensure that we don't have too many connections from the same IP address.
            if self.socket_handler.is_max_connections(connection.address):
                await connection.reject('toomany')
                return

        # Create the player instance finally.
        log.info(f"Player instance would be created here for {connection.address}")
        # TODO: new Player(self.world, self.database, connection)

    def get_last_connection(self, connection: Connection) -> int:
        address_info = self.socket_handler.addresses.get(connection.address)
        return address_info.last_time if address_info else 0

    def create_packet_queue(self, instance: str):
        self.packets[instance] = []

    def delete_packet_queue(self, instance: str):
        if instance in self.packets:
            del self.packets[instance]

    # Broadcasting and Socket Communication

    def broadcast(self, packet: Any):
        """
        Broadcasts a packet to the entire server.
        """
        # Original: serializedPacket = packet.serialize()
        # For now we assume packet is already something we can send or has a serialize method
        serialized = packet.serialize() if hasattr(packet, 'serialize') else packet
        
        for queue in self.packets.values():
            queue.append(serialized)

    def send(self, instance: str, packet: Any):
        """
        Send a packet to a player's connection.
        """
        if instance not in self.packets:
            return

        serialized = packet.serialize() if hasattr(packet, 'serialize') else packet
        self.packets[instance].append(serialized)

    def send_to_players(self, instances: List[str], packet: Any):
        for instance in instances:
            self.send(instance, packet)

    def send_to_region(self, region_id: int, packet: Any, ignore: Optional[str] = None):
        if not self.regions:
            return
            
        # TODO: Implement region logic when Regions class is available
        pass

    def send_to_surrounding_regions(self, region_id: int, packet: Any, ignore: Optional[str] = None):
        if region_id < 0 or not self.regions:
            return
            
        # TODO: Implement surrounding region logic
        pass
