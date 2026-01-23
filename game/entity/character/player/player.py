from common.log import log
from game.entity.character.character import Character
from game.world import World
from network import EntityData
from network.connection import Connection
from network.impl.connected import ConnectedPacket
from network.packet import Packet


class Player(Character):

    def __init__(self, world: World, connection: Connection):
        super().__init__(connection.instance, world, "", -1, -1)

        self.world = world
        self.connection = connection

        self.connection.on_close(self.handle_close)

        # Send the connected packet, begin the handshake process.
        self.send(ConnectedPacket())

    def handle_close(self) -> None:
        log.info(f"Closing player: {self.connection.address}")
        self.stop_intervals()

    def send(self, packet: Packet) -> None:
        self.world.network_manager.send(self.connection.instance, packet)

    def serialize(self, with_equipment: bool = False, with_experience: bool = False,
                  with_mana: bool = False) -> EntityData:
        data = super().serialize()

        return data
