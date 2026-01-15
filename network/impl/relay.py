from typing import Any, List
from ..packet import Packet
from ..packets import Packets

class RelayPacket(Packet):
    def __init__(self, username: str, packet: Packet):
        serialized_packet = packet.serialize()
        # serialized_packet is [id, data] or [id, opcode, data] (+ optionally buffer_size)
        # We need to construct [username, *serialized_packet]
        data: List[Any] = [username]
        data.extend(serialized_packet)

        super().__init__(id=Packets.Relay, data=data)
