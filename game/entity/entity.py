from abc import ABC, abstractmethod
from typing import List, Optional, Callable, Any, Union
import math

from network.modules import EntityType, ResourceState, Orientation
from network.shared_types import EntityData, EntityDisplayInfo

# Type alias for better readability
MovementCallback = Callable[[int, int], None]

class Entity(ABC):
    """
    An abstract class for every entity in the game. The `instance`
    represents a unique ID assigned to each entity. `key` represents
    the entity's data identification (and image file name).
    """

    def __init__(self, instance: str = "", key: str = "", x: int = -1, y: int = -1):
        self.instance = instance
        self.key = key
        
        self.type: int = self._get_entity_type(self.instance)
        self.name: str = ""

        self.x: int = x
        self.y: int = y

        self.old_x: int = -1
        self.old_y: int = -1

        self.dead: bool = False

        self.region: int = -1
        self.colour: str = ""  # name colour displayed for the entity
        self.scale: float = 0.0  # scale of the entity (default if not specified)
        self.visible: bool = True  # used to hide an entity from being sent to the client.

        self.recent_regions: List[int] = []  # regions the entity just left

        self.movement_callback: Optional[MovementCallback] = None

        self.update_position(x, y)

    def _get_entity_type(self, instance: str) -> int:
        """
        Extracts the type of entity by taking the first part of the instance ID.
        In TypeScript: parseInt(instance.split('-')[0])
        """
        if not instance or "-" not in instance:
            return -1
        try:
            return int(instance.split("-")[0])
        except (ValueError, IndexError):
            return -1

    def set_position(self, x: int, y: int) -> None:
        """
        Updates the entity's position in the grid. We also store
        the previous position for the entity prior to updating.
        :param x: The new x grid position.
        :param y: The new y grid position.
        """
        # On initialization just set oldX/Y to the current position
        self.old_x = self.x
        self.old_y = self.y

        self.x = x
        self.y = y

        # Make a callback
        if self.movement_callback:
            self.movement_callback(x, y)

    # TODO: Get rid of the method as it's not needed in the Python implementation
    def update_position(self, x: int, y: int) -> None:
        """
        This is an external set position function used when initializing an entity.
        This prevents any whacky subclass calls to `setPosition` when we first create
        the entity.
        :param x: The new x grid position.
        :param y: The new y grid position.
        """
        self.old_x = x if self.x == -1 else self.x
        self.old_y = y if self.y == -1 else self.y

        self.x = x
        self.y = y

    def set_region(self, region: int) -> None:
        """
        Update the entity's position.
        :param region: The new region we are setting.
        """
        self.region = region

    def set_recent_regions(self, regions: List[int]) -> None:
        """
        Replaces the array indicating recently left regions with a new array.
        :param regions: The new array of recent regions the entity left from.
        """
        self.recent_regions = regions

    def get_distance(self, entity: "Entity") -> int:
        """
        Finds the distance between the current entity object and the
        specified entity parameter.
        :param entity: Entity we are finding distance of.
        :returns: The approximate distance in tiles between entities.
        """
        return abs(self.x - entity.x) + abs(self.y - entity.y)

    def get_display_info(self, _var1: Any = None) -> EntityDisplayInfo:
        """
        Superclass implementation for grabbing the display info. We provide the
        player with the bare minimum in case this function gets called without
        the entity actually containing alternate display info.
        :param _var1: Optional parameter used in the subclasses.
        :returns: A EntityDisplayInfo object containing the instance of the entity.
        """
        return EntityDisplayInfo(instance=self.instance)

    def has_display_info(self, _var1: Any = None) -> bool:
        """
        A superclass implementation for whether or not an entity
        contains update data. For example, a mob may be contain
        this data if it is part of an area or is a quest-based mob.
        Display info refers to slight alterations to an entity's appearance.
        This can be a different colour for their name, or a different scale.
        :param _var1: Optional parameter used by the subclasses.
        """
        return False

    def is_near(self, entity: "Entity", distance: int) -> bool:
        """
        Checks the distance between the current entity object and another
        specified entity. The distance parameter specifies how far the other
        entity can be for us to return true.
        :param entity: The entity we are comparing against.
        :param distance: The offset distance we are looking for.
        :returns: Whether the `entity` parameter is `distance` or closer to our entity.
        """
        dx = abs(self.x - entity.x)
        dy = abs(self.y - entity.y)

        return dx <= distance and dy <= distance

    def is_adjacent(self, entity: "Entity") -> bool:
        """
        Checks if an entity is next to the current entity object.
        :param entity: Entity we are checking distance of.
        :returns: Whether the distance of the entity we are checking is at MOST 1 block away.
        """
        return self.get_distance(entity) < 2

    def is_non_diagonal(self, entity: "Entity") -> bool:
        """
        Checks if the other entity is next to the current entity but not diagonally adjacent.
        :param entity: Entity we are checking.
        :returns: That the entity is either up, right, left, or down of this entity object.
        """
        return self.is_adjacent(entity) and not (entity.x != self.x and entity.y != self.y)

    def is_visible(self, player: Optional[Any] = None) -> bool:
        """
        Returns whether or not the entity is visible. An entity may be hidden when
        an admin wants to not be shown to other players, or when a player finishes
        a quest, and we may want to hide an NPC.
        :param player: An optional parameter is used to check if the player has finished
        a quest associated with the entity.
        :returns: Whether the entity is visible.
        """
        # Return visibility status if no player provided or entity is not an NPC.
        if not player or not self.is_npc():
            return self.visible

        # TODO: Implement quest visibility check once Quests and Player are implemented.
        # quest = player.quests.get_quest_from_npc(self, True)
        # if not quest:
        #     return self.visible
        # return quest.is_npc_visible(self.key)
        
        return self.visible

    # Type checking methods

    def is_character(self) -> bool:
        """
        Used to check whether the entity is a character that can move and perform combat.
        :returns: Whether the entity is a character.
        """
        from game.entity.character.character import Character
        return isinstance(self, Character)

    def is_mob(self) -> bool:
        """
        Checks whether the entity's type is a mob.
        :returns: Whether the type is equal to the EntityType mob.
        """
        return self.type == EntityType.Mob

    def is_npc(self) -> bool:
        """
        Checks whether the entity's type is a NPC.
        :returns: Whether the type is equal to the EntityType NPC.
        """
        return self.type == EntityType.NPC

    def is_item(self) -> bool:
        """
        Checks whether the entity's type is a item.
        :returns: Whether the type is equal to the EntityType item.
        """
        return self.type == EntityType.Item

    def is_loot_bag(self) -> bool:
        """
        Checks whether the entity's type is a loot bag.
        :returns: Whether the type is equal to the EntityType loot bag.
        """
        return self.type == EntityType.LootBag

    def is_chest(self) -> bool:
        """
        Checks whether the entity's type is a chest.
        :returns: Whether the type is equal to the EntityType chest.
        """
        return self.type == EntityType.Chest

    def is_player(self) -> bool:
        """
        Checks whether the entity's type is a player.
        :returns: Whether the type is equal to the EntityType player.
        """
        return self.type == EntityType.Player

    def is_projectile(self) -> bool:
        """
        Checks whether or not the entity is a projectile.
        :returns: Whether the type is equal to the EntityType projectile.
        """
        return self.type == EntityType.Projectile

    def is_pet(self) -> bool:
        """
        Checks whether or not the entity is a pet.
        :returns: Whether the type is equal to the EntityType pet.
        """
        return self.type == EntityType.Pet

    def is_effect(self) -> bool:
        """
        Checks whether or not the entity is an effect.
        :returns: Whether the type is equal to the EntityType effect.
        """
        return self.type == EntityType.Effect

    def is_tree(self) -> bool:
        """
        Checks whether or not the entity is a tree.
        :returns: Whether the type is equal to the EntityType tree.
        """
        return self.type == EntityType.Tree

    def is_rock(self) -> bool:
        """
        Checks whether or not the entity is a rock.
        :returns: Whether the type is equal to the EntityType rock.
        """
        return self.type == EntityType.Rock

    def is_fish_spot(self) -> bool:
        """
        Checks whether or not the entity is a fish spot.
        :returns: Whether the type is equal to the EntityType fish spot.
        """
        return self.type == EntityType.FishSpot

    def is_foraging(self) -> bool:
        """
        Checks whether or not the entity is a foraging spot.
        :returns: Whether the type is equal to the EntityType foraging spot.
        """
        return self.type == EntityType.Foraging

    def is_resource(self) -> bool:
        """
        Checks whether or not the entity is a resource.
        :returns: Whether the entity is a tree, rock, fish spot, or foraging spot.
        """
        return self.is_tree() or self.is_rock() or self.is_fish_spot() or self.is_foraging()

    def serialize(self) -> EntityData:
        """
        This is entity superclass serialization. It provides
        the absolute most basic data about the entity. Entities
        that extend the Entity class will use this to get initial data
        and add more information on top.
        :returns: Basic data about the entity like its instance, type, and position.
        """
        return EntityData(
            instance=self.instance,
            type=self.type,
            name=self.name,
            key=self.key,
            x=self.x,
            y=self.y
        )

    def on_movement(self, callback: MovementCallback) -> None:
        """
        Callback every time there is a change in the absolute position.
        """
        self.movement_callback = callback
