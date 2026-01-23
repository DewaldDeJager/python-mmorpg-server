from common.log import log
from game.entity.character.character import Character
from game.world import World
from network import EntityData
from network.connection import Connection
from network.impl.connected import ConnectedPacket
from game.packet_data import PacketData
from network.modules import PacketType
from network.packet import Packet
from game.entity.character.player.incoming import Incoming


class Player(Character):

    def __init__(self, world: World, connection: Connection):
        super().__init__(connection.instance, world, "", -1, -1)

        self.world = world
        self.connection = connection

        self.incoming = Incoming(self)

        self.connection.on_close(self.handle_close)

        # Send the connected packet, begin the handshake process.
        self.send(ConnectedPacket())

    def handle_close(self) -> None:
        log.info(f"Closing player: {self.connection.address}")
        self.stop_intervals()

    def send(self, packet: Packet) -> None:
        """
        We create this function to make it easier to send
        packets to players instead of always importing `world`
        in other classes.
        @param packet Packet we are sending to the player.
        """
        self.world.push(PacketType.Player, PacketData(packet=packet, player=self))

    def serialize(self, with_equipment: bool = False, with_experience: bool = False,
                  with_mana: bool = False) -> EntityData:
        data = super().serialize()

        return data


PacketData.model_rebuild()
