import time
from typing import List, Optional, Callable, Dict, Any, Union

from game.entity.entity import Entity
from game.info.formulas import Formulas
from game.world import World
from game.entity.character.points.hitpoints import HitPoints
from game.entity.character.effect.poison import Poison
from game.entity.character.effect.status import Status
from game.entity.character.combat.hit import Hit
from network.packet import Packet
from network.modules import Constants, Defaults, Orientation, Hits, Effects
from network.shared_types import EntityData, Stats, Bonuses

# Type aliases for better readability
PoisonCallback = Callable[[int, bool], None]
HitCallback = Callable[[int, Optional["Character"], bool], None]
DeathCallback = Callable[[Optional["Character"]], None]


class Character(Entity):
    def __init__(self, instance: str, world: World, key: str, x: int, y: int):
        super().__init__(instance, key, x, y)

        self.world = world
        self.level = 1
        self.attack_range = 1
        self.plateau_level = 0

        # self.combat: Combat # Excluded as per instructions
        # TODO: Implement combat
        self.hit_points = HitPoints(Formulas.get_max_hit_points(self.level))

        self.heal_rate: int = Constants.HEAL_RATE
        self.movement_speed: int = Defaults.MOVEMENT_SPEED
        self.attack_rate: int = Defaults.ATTACK_RATE
        self.orientation: Orientation = Orientation.Down
        self.damage_type: Hits = Hits.Normal

        # States
        self.poison: Optional[Poison] = None
        self.status: Status = Status()

        # Character that is currently being targeted.
        self.target: Optional["Character"] = None

        # List of entities attacking this character.
        # Used by combat to determine which character to target.
        self.attackers: List["Character"] = []

        self.damage_table: Dict[str, int] = {}

        self.moving = False
        self.pvp = False
        self.teleporting = False
        self.aoe = 0

        # Effects applied onto the character.
        self.status_effects: List[Effects] = []

        self.projectile_name = 'arrow'

        self.last_step = -1
        self.last_movement = int(time.time() * 1000)
        self.last_region_change = -1

        # Intervals are excluded as per instructions
        # TODO: Add the intervals

        self.poison_callback: Optional[PoisonCallback] = None
        self.hit_callback: Optional[HitCallback] = None
        self.death_callback: Optional[DeathCallback] = None
        self.death_i_callback: Optional[DeathCallback] = None

        # Initialization logic from TS constructor
        self.hit_points.on_hit_points(self.handle_hit_points)

        self.status.on_add(self.handle_status_effect_add)
        self.status.on_remove(self.handle_status_effect_remove)

        # setIntervals for healing and effects are excluded

    def handle_hit_points(self) -> None:
        """
        Handles a change in the hit points and relays
        that information to the nearby regions.
        """
        pass

    def handle_status_effect_add(self, effect: Effects) -> None:
        """
        Handles the addition of a status effect.
        """
        pass

    def handle_status_effect_remove(self, effect: Effects) -> None:
        """
        Handles the removal of a status effect.
        """
        pass

    def handle_poison(self) -> None:
        """
        Handles the poison effect.
        """
        pass

    def handle_aoe(self, damage: int, attacker: "Character", range_val: int) -> None:
        """
        Handles the area of effect damage.
        """
        pass

    def handle_cold_damage(self) -> None:
        """
        Handles the cold damage.
        """
        pass

    def handle_burning_damage(self) -> None:
        """
        Handles the burning damage.
        """
        pass

    def handle_poison_damage(self, attacker: "Character") -> None:
        """
        Handles the poison damage.
        """
        pass

    def handle_bloodsucking(self, attacker: "Character", damage: int) -> None:
        """
        Handles the bloodsucking effect.
        """
        pass

    def heal(self, amount: int) -> None:
        """
        Heals the character.
        """
        pass

    def effects(self) -> None:
        """
        Handles the effects.
        """
        pass

    def find_adjacent_tile(self) -> Dict[str, int]:
        """
        Finds an adjacent tile.
        """
        return {"x": -1, "y": -1}

    def stop(self) -> None:
        """
        Stops the character.
        """
        pass

    def hit(self, damage: int, attacker: Optional["Character"] = None, aoe: int = 0, is_thorns: bool = False) -> None:
        """
        Handles the hit.
        """
        pass

    def follow(self, target: Optional["Character"] = None) -> None:
        """
        Follows the target.
        """
        pass

    def teleport(self, x: int, y: int, with_animation: bool = False) -> None:
        """
        Teleports the character.
        """
        pass

    def countdown(self, time_val: int) -> None:
        """
        Handles the countdown.
        """
        pass

    def stop_movement(self) -> None:
        """
        Stops the character's movement.
        """
        pass

    def clear_target(self) -> None:
        """
        Clears the target.
        """
        pass

    def clear_attackers(self) -> None:
        """
        Clears the attackers.
        """
        pass

    def remove_attacker(self, attacker: "Character") -> None:
        """
        Removes an attacker.
        """
        pass

    def get_attacker_count(self) -> int:
        """
        Gets the attacker count.
        """
        return 0

    def get_attack_rate(self) -> int:
        """
        Gets the attack rate.
        """
        return 0

    def get_attack_stats(self) -> Stats:
        """
        Gets the attack stats.
        """
        return Stats()

    def get_defense_stats(self) -> Stats:
        """
        Gets the defense stats.
        """
        return Stats()

    def get_bonuses(self) -> Bonuses:
        """
        Gets the bonuses.
        """
        return Bonuses()

    def get_accuracy_bonus(self) -> int:
        """
        Gets the accuracy bonus.
        """
        return 0

    def get_accuracy_level(self) -> int:
        """
        Gets the accuracy level.
        """
        return 0

    def get_strength_level(self) -> int:
        """
        Gets the strength level.
        """
        return 0

    def get_archery_level(self) -> int:
        """
        Gets the archery level.
        """
        return 0

    def get_defense_level(self) -> int:
        """
        Gets the defense level.
        """
        return 0

    def get_damage_bonus(self) -> int:
        """
        Gets the damage bonus.
        """
        return 0

    def get_skill_damage_level(self) -> int:
        """
        Gets the skill damage level.
        """
        return 0

    def get_damage_reduction(self) -> int:
        """
        Gets the damage reduction.
        """
        return 0

    def get_attack_style(self) -> Hits:
        """
        Gets the attack style.
        """
        return Hits.Normal

    def get_damage_type(self) -> Hits:
        """
        Gets the damage type.
        """
        return Hits.Normal

    def get_poison_chance(self) -> int:
        """
        Gets the poison chance.
        """
        return 0

    def get_random_attacker(self) -> Optional["Character"]:
        """
        Gets a random attacker.
        """
        return None

    def get_aoe(self) -> int:
        """
        Gets the aoe.
        """
        return 0

    def get_projectile_name(self) -> str:
        """
        Gets the projectile name.
        """
        return ""

    def get_last_attack(self) -> int:
        """
        Gets the last attack.
        """
        return 0

    def get_bloodsucking_level(self) -> int:
        """
        Gets the bloodsucking level.
        """
        return 0

    def has_special_attack(self) -> bool:
        """
        Checks if the character has a special attack.
        """
        return False

    def has_target(self) -> bool:
        """
        Checks if the character has a target.
        """
        return False

    def has_attacker(self, attacker: "Character") -> bool:
        """
        Checks if the character has an attacker.
        """
        return False

    def has_arrows(self) -> bool:
        """
        Checks if the character has arrows.
        """
        return False

    def has_bloodsucking(self) -> bool:
        """
        Checks if the character has bloodsucking.
        """
        return False

    def in_combat(self) -> bool:
        """
        Checks if the character is in combat.
        """
        return False

    def is_ranged(self) -> bool:
        """
        Checks if the character is ranged.
        """
        return False

    def is_archer(self) -> bool:
        """
        Checks if the character is an archer.
        """
        return False

    def is_magic(self) -> bool:
        """
        Checks if the character is magic.
        """
        return False

    def is_dead(self) -> bool:
        """
        Checks if the character is dead.
        """
        return False

    def is_near_target(self) -> bool:
        """
        Checks if the character is near the target.
        """
        return False

    def is_poisonous(self) -> bool:
        """
        Checks if the character is poisonous.
        """
        return False

    def is_on_same_tile(self) -> bool:
        """
        Checks if the character is on the same tile.
        """
        return False

    def is_stunned(self) -> bool:
        """
        Checks if the character is stunned.
        """
        return False

    def can_attack(self, target: "Character") -> bool:
        """
        Checks if the character can attack the target.
        """
        return False

    def set_position(self, x: int, y: int, with_teleport: bool = False) -> None:
        """
        Sets the character's position.
        """
        super().set_position(x, y)

    def set_target(self, target: "Character") -> None:
        """
        Sets the character's target.
        """
        pass

    def add_attacker(self, attacker: "Character") -> None:
        """
        Adds an attacker.
        """
        pass

    def add_to_damage_table(self, attacker: "Character", damage: int) -> None:
        """
        Adds to the damage table.
        """
        pass

    def add_status_effect(self, hit: Hit) -> None:
        """
        Adds a status effect.
        """
        pass

    def find_nearest_target(self) -> Optional["Character"]:
        """
        Finds the nearest target.
        """
        return None

    def set_hit_points(self, hit_points: int) -> None:
        """
        Sets the hit points.
        """
        pass

    # TODO: Consider using better types for the arguments, like the PoisonTypes enum for type_val
    def set_poison(self, type_val: int = -1, start: Optional[int] = None) -> None:
        """
        Sets the poison effect.
        """
        pass

    def set_orientation(self, orientation: Orientation) -> None:
        """
        Sets the orientation.
        """
        pass

    def send_to_region(self, packet: Packet, ignore: bool = False) -> None:
        """
        Sends a packet to the region.
        """
        pass

    def send_to_regions(self, packet: Packet, ignore: bool = False) -> None:
        """
        Sends a packet to the regions.
        """
        pass

    def send_broadcast(self, packet: Packet) -> None:
        """
        Sends a broadcast packet.
        """
        pass

    def for_each_nearby_character(self, callback: Callable[["Character"], None], range_val: int = 1) -> None:
        """
        Iterates through each nearby character.
        """
        pass

    def for_each_attacker(self, callback: Callable[["Character"], None]) -> None:
        """
        Iterates through each attacker.
        """
        pass

    def serialize(self) -> EntityData:
        """
        Serializes the character.
        """
        return super().serialize()

    def on_poison(self, callback: PoisonCallback) -> None:
        """
        Callback for when the character is poisoned.
        """
        pass

    def on_hit(self, callback: HitCallback) -> None:
        """
        Callback for when the character is hit.
        """
        pass

    def on_death(self, callback: DeathCallback) -> None:
        """
        Callback for when the character dies.
        """
        pass

    def on_death_impl(self, callback: DeathCallback) -> None:
        """
        Implementation for the death callback.
        """
        pass
