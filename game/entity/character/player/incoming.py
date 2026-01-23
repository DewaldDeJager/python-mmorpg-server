from __future__ import annotations
from typing import TYPE_CHECKING, Any, Dict, List, Optional
import time

from common.config import config
from common.log import log
from network.impl.handshake import HandshakePacket, ClientHandshakePacketData
from network.packets import Packets

if TYPE_CHECKING:
    from game.entity.character.player.player import Player
    from game.world import World
    from network.connection import Connection


class Incoming:
    def __init__(self, player: Player):
        self.player = player
        self.connection: Connection = player.connection
        self.world: World = player.world

        self.completed_handshake = False

        self.connection.on_message(self.handle_message)

    def handle_message(self, message: Any):
        # TODO: Improve the validation and type checking
        # The message is typically a list [packet_id, data] or [packet_id, opcode, data]
        if not isinstance(message, list) or len(message) < 2:
            log.error(f"Invalid message format received: {message}")
            return

        packet_id = -1
        data = None
        if len(message) == 2:
            packet_id, data = message
        elif len(message) == 3:
            packet_id, opcode, data = message

        try:
            if not self.completed_handshake and packet_id != Packets.Handshake:
                log.warning(f"Received packet {packet_id} before handshake was completed.")
                return
            if packet_id == Packets.Handshake:
                self.handle_handshake(data)
            elif packet_id == Packets.Login:
                pass
            elif packet_id == Packets.Ready:
                pass

        except Exception as e:
            log.error(f"Error handling packet {packet_id}: {e}")

    def handle_handshake(self, data: Dict[str, Any]):
        """
        The handshake is responsible for verifying the integrity of the client initially.
        We ensure that the client is on the right version and reject it if it is not.
        """
        game_version = data.get("gVer")
        
        if game_version != config.gver:
            log.warning(f"Client version mismatch: {game_version} != {config.gver}")
            # In Connection.py, reject is async, but we are in a sync callback.
            # However, Incoming in TS is also sync and it calls connection.reject which might be async there too.
            # In our main.py, it's called in an async loop.
            import asyncio
            asyncio.create_task(self.connection.reject("updated"))
            return

        self.completed_handshake = True

        # Immediately send the handshake packet by bypassing the queue so that server time is accurate.
        handshake_data = ClientHandshakePacketData(
            type="client",
            instance=self.player.instance,
            server_id=config.server_id,
            server_time=int(time.time() * 1000) # Using milliseconds
        )
        
        import asyncio
        asyncio.create_task(self.connection.send([HandshakePacket(handshake_data).serialize()]))
