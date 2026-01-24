from __future__ import annotations
from typing import TYPE_CHECKING, Any, Dict, List, Optional
import time

from common.config import config
from common.log import log
from common.utils import Utils
from database.mongodb_creator import Creator
from network import Login
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

    async def handle_message(self, message: Any):
        # TODO: Improve the validation and type checking
        # The message is typically a list [packet_id, data] or [packet_id, opcode, data]
        if not isinstance(message, list) or len(message) < 2:
            log.error(f"Invalid message format received: {message}")
            return

        # Example message: [2, {'opcode': 2, 'foo': 'bar'}]
        packet_id = message[0]
        data = message[1] if len(message) > 1 else None

        self.connection.refresh_timeout()

        try:
            if not self.completed_handshake and packet_id != Packets.Handshake:
                log.warning(f"Received packet {packet_id} before handshake was completed.")
                await self.connection.reject("lost")
            if packet_id == Packets.Handshake:
                await self.handle_handshake(data)
            elif packet_id == Packets.Login:
                await self.handle_login(data)
            elif packet_id == Packets.Ready:
                pass
            elif packet_id == Packets.Focus:
                pass
            else:
                log.warning(f"Received unknown packet {packet_id}.")

        except Exception as e:
            log.error(f"Error handling packet {packet_id}: {e}")

    async def handle_handshake(self, data: Dict[str, Any]):
        """
        The handshake is responsible for verifying the integrity of the client initially.
        We ensure that the client is on the right version and reject it if it is not.
        """
        game_version = data.get("gVer")
        
        if game_version != config.gver:
            log.warning(f"Client version mismatch: {game_version} != {config.gver}")
            await self.connection.reject("updated")
            return

        self.completed_handshake = True

        # Immediately send the handshake packet by bypassing the queue so that server time is accurate.
        handshake_data = ClientHandshakePacketData(
            type="client",
            instance=self.player.instance,
            server_id=config.server_id,
            server_time=int(time.time() * 1000) # Using milliseconds
        )
        
        await self.connection.send([HandshakePacket(handshake_data).serialize()])

    async def handle_login(self, data: Dict[str, Any]):
        # Login example: [{'opcode': 0, 'password': 'password', 'username': 'DearVolt'}]
        # Register example: [{'opcode': 0, 'password': 'password', 'username': 'DearVolt', 'email': 'example@example.com'}]
        # Guest example: [{'opcode': 2}]
        opcode = data.get("opcode")
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")

        if opcode == Login.Login:
            log.notice(f"Login request received with {data=}.")
            pass
        elif opcode == Login.Register:
            log.notice(f"Register request received with {data=}.")
        elif opcode == Login.Guest:
            log.notice("Guest login request received.")
            self.player.authenticated = True
            self.player.is_guest = True
            self.player.username = Utils.get_guest_username()

            await self.player.load(Creator.serialize(self.player))
        else:
            log.warning(f"Received unknown login opcode {opcode}.")
