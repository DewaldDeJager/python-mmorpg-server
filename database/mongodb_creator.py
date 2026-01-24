from __future__ import annotations
from typing import TYPE_CHECKING
from common.config import config
from database.models.player import PlayerInfo, PoisonInfo

if TYPE_CHECKING:
    from game.entity.character.player.player import Player

class Creator:
    """
    The Creator class is responsible for creating and saving new data to the database,
    such as new players or world state changes.
    """
    def __init__(self, database=None):
        self.database = database

    @staticmethod
    def serialize(player: Player) -> PlayerInfo:
        """
        Serializes a player object and extracts all the basic information
        that will be saved in the database. This is generally used for
        loading the player and sending the preliminary information to the client.
        @param player The player object that we want to serialize.
        @returns A serialized object that contains the player's information, we use
        this and store it in the database.
        """
        return PlayerInfo(
            username=player.username,
            password=player.password,
            email=player.email,
            x=player.x,
            y=player.y,
            user_agent=player.user_agent,
            rank=player.rank,
            poison=PoisonInfo(
                type=player.poison.type.value if player.poison and player.poison.type else -1,
                remaining=int(player.poison.get_remaining_time()) if player.poison else -1
            ) if player.poison is not None else None,
            effects={}, # player.status.serialize() - Not yet implemented
            hit_points=player.hit_points.get_hit_points(),
            mana=player.mana.get_mana(),
            orientation=player.orientation,
            ban=player.ban,
            mute=player.mute,
            jail=player.jail,
            last_warp=player.last_warp,
            map_version=player.map_version,
            regions_loaded=player.regions_loaded,
            friends=[], # player.friends.serialize() - Not yet implemented
            last_server_id=config.server_id,
            last_address=player.connection.address,
            last_global_chat=0, # player.last_global_chat - Not yet implemented
            guild=player.guild,
            pet="" # player.pet.key if player.pet else "" - Not yet implemented
        )
