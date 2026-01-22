import time
import random
import math
import asyncio
from abc import abstractmethod
from datetime import datetime
from typing import List, Optional, Callable, Dict, override, Any

from common.utils import Utils
from game.entity.entity import Entity
from game.info.formulas import Formulas
from game.entity.character.points.hitpoints import HitPoints
from game.entity.character.effect.poison import Poison
from game.entity.character.effect.status import Status
from game.entity.character.combat.hit import Hit
from network.packet import Packet
from network.modules import Constants, Defaults, Orientation, Hits, Effects, PacketType, PoisonTypes
from network.shared_types import EntityData, Stats, Bonuses
from network import opcodes as Opcodes, AttackStyle

from game.world import World, PacketData
from network.impl.movement import MovementPacket, MovementPacketData
from network.impl.teleport import TeleportPacket, TeleportPacketData
from network.impl.points import PointsPacket, PointsPacketData
from network.impl.combat import CombatPacket, CombatPacketData
from network.impl.effect import EffectPacket, EffectPacketData
from network.impl.countdown import CountdownPacket, CountdownPacketData

# Type aliases for better readability
PoisonCallback = Callable[[Optional[PoisonTypes], bool], None]
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

        self.healing_task: Optional[asyncio.Task] = None
        self.effect_task: Optional[asyncio.Task] = None
        self.poison_task: Optional[asyncio.Task] = None

        self.poison_callback: Optional[PoisonCallback] = None
        self.hit_callback: Optional[HitCallback] = None
        self.death_callback: Optional[DeathCallback] = None
        self.death_i_callback: Optional[DeathCallback] = None

        # Initialization logic from TS constructor
        self.hit_points.on_hit_points(self.handle_hit_points)

        self.status.on_add(self.handle_status_effect_add)
        self.status.on_remove(self.handle_status_effect_remove)

        self.start_intervals()

    def start_intervals(self) -> None:
        """
        Starts the periodic intervals for the character.
        """
        self.healing_task = asyncio.create_task(self._interval_loop(self.heal, self.heal_rate / 1000.0))
        self.effect_task = asyncio.create_task(self._interval_loop(self.effects, Constants.EFFECT_RATE / 1000.0))

    def stop_intervals(self) -> None:
        """
        Stops all active interval tasks.
        """
        if self.healing_task:
            self.healing_task.cancel()
            self.healing_task = None

        if self.effect_task:
            self.effect_task.cancel()
            self.effect_task = None

        self.stop_poison_interval()

    def start_poison_interval(self) -> None:
        """
        Starts the poison interval task.
        """
        if self.poison:
            self.poison_task = asyncio.create_task(self._interval_loop(self.handle_poison, self.poison.rate.total_seconds()))

    def stop_poison_interval(self) -> None:
        """
        Stops the poison interval task.
        """
        if self.poison_task:
            self.poison_task.cancel()
            self.poison_task = None

    async def _interval_loop(self, callback: Callable[[], Any], interval: float) -> None:
        """
        A helper method to run a callback periodically.
        """
        try:
            while True:
                await asyncio.sleep(interval)
                callback()
        except asyncio.CancelledError:
            pass

    def handle_hit_points(self) -> None:
        """
        Handles a change in the hit points and relays
        that information to the nearby regions.
        """
        self.send_to_regions(
            PointsPacket(
                PointsPacketData(
                    instance=self.instance,
                    hit_points=self.hit_points.get_hit_points(),
                    max_hit_points=self.hit_points.get_max_hit_points()
                )
            )
        )

    def handle_status_effect_add(self, effect: Effects) -> None:
        """
        Handles the addition of a status effect.
        """
        if self.is_player() and effect == Effects.Freezing:
            # TODO: Implement sync()
            # self.sync()
            pass

        self.send_to_regions(
            EffectPacket(
                Opcodes.Effect.Add,
                EffectPacketData(instance=self.instance, effect=effect)
            )
        )

    def handle_status_effect_remove(self, effect: Effects) -> None:
        """
        Handles the removal of a status effect.
        """
        if self.is_player() and effect == Effects.Freezing:
            # TODO: Implement sync() and in_freezing_area()
            # self.sync()
            # if self.in_freezing_area():
            #     return self.status.add(Effects.Freezing)
            pass

        self.send_to_regions(
            EffectPacket(
                Opcodes.Effect.Remove,
                EffectPacketData(instance=self.instance, effect=effect)
            )
        )

    def handle_poison(self) -> None:
        """
        Handles the poison effect.
        """
        if not self.poison:
            return None

        # Remove the poison if it has expired.
        if self.poison.expired():
            return self.set_poison()

        # Create a hit object for poison damage and serialize it.
        hit_data = Hit(Hits.Poison, self.poison.damage).serialize()

        # Send a hit packet to display the info to the client.
        self.send_to_regions(
            CombatPacket(
                Opcodes.Combat.Hit,
                CombatPacketData(
                    instance=self.instance,
                    target=self.instance,
                    hit=hit_data
                )
            )
        )

        # Do the actual damage to the character.
        self.hit(self.poison.damage)

    def handle_aoe(self, damage: int, attacker: Optional["Character"] = None, range_val: int = 1) -> None:
        """
        Handles the area of effect damage.
        """
        def aoe_callback(character: "Character") -> None:
            distance = self.get_distance(character) + 1
            hit = Hit(
                Hits.Normal,
                math.floor(damage / distance),
                False,
                distance
            )
            hit_data = hit.serialize()

            # Create a hit packet and send it to the nearby regions.
            self.send_to_regions(
                CombatPacket(
                    Opcodes.Combat.Hit,
                    CombatPacketData(
                        instance=attacker.instance if attacker else '',
                        target=character.instance,
                        hit=hit_data
                    )
                )
            )

            # Apply the damage to the character.
            character.hit(hit.damage, attacker)

        self.for_each_nearby_character(aoe_callback, range_val)

    def handle_cold_damage(self) -> None:
        """
        Handles the cold damage.
        """
        # Only players that do not have the snow potion can be affected.
        if self.status.has(Effects.SnowPotion):
            return

        # Create a hit object for cold damage and serialize it.
        hit_data = Hit(Hits.Freezing, Constants.COLD_EFFECT_DAMAGE).serialize()

        # Send a hit packet to display the info to the client.
        self.send_to_regions(
            CombatPacket(
                Opcodes.Combat.Hit,
                CombatPacketData(
                    instance=self.instance,
                    target=self.instance,
                    hit=hit_data
                )
            )
        )

        # Do the actual damage to the character.
        self.hit(Constants.COLD_EFFECT_DAMAGE)

    def handle_burning_damage(self) -> None:
        """
        Handles the burning damage.
        """
        # Only players that do not have the fire potion can be affected.
        if self.status.has(Effects.FirePotion):
            return

        # Create a hit object for burning damage and serialize it.
        hit_data = Hit(Hits.Burning, Constants.BURNING_EFFECT_DAMAGE).serialize()

        # Send a hit packet to display the info to the client.
        self.send_to_regions(
            CombatPacket(
                Opcodes.Combat.Hit,
                CombatPacketData(
                    instance=self.instance,
                    target=self.instance,
                    hit=hit_data
                )
            )
        )

        # Do the actual damage to the character.
        self.hit(Constants.BURNING_EFFECT_DAMAGE)

    def handle_poison_damage(self, attacker: "Character") -> None:
        """
        Handles the poison damage.
        """
        # Poison is related to the strength or archery level.
        is_poisoned = Formulas.get_poison_chance(self.get_skill_damage_level()) < attacker.get_poison_chance()

        # Use venom as default for now.
        if is_poisoned:
            self.set_poison(PoisonTypes.Venom)

    def handle_bloodsucking(self, attacker: "Character", damage: int) -> None:
        """
        Handles the bloodsucking effect.
        """
        # Blood sucking has a 30% chance of occurring, so we return 70% of the time.
        if random.randint(0, 100) > 30:
            return

        # 5% of the damage dealt per level of bloodsucking is healed.
        heal_amount = math.floor(damage * (0.05 * attacker.get_bloodsucking_level()))

        # Prevent healing if the amount is less than 1.
        if heal_amount < 1:
            return

        if attacker.is_player():
            # TODO: Implement heal() with type
            # attacker.heal(heal_amount, 'hitpoints')
            attacker.heal(heal_amount)
        else:
            attacker.heal(heal_amount)

    def heal(self, amount: int = 1) -> None:
        """
        Heals the character.
        """
        # Cannot heal if dead or poisoned.
        if self.is_dead() or self.poison:
            return

        # TODO: Implement combat started check
        # if self.combat.started:
        #     return

        # Cannot heal if character is being attacked.
        if self.get_attacker_count() > 0:
            return

        # Stops the character from healing if they are at max hitpoints.
        if self.hit_points.is_full():
            return

        # Certain status effects prevent the character from healing.
        if (self.status.has(Effects.Freezing) or
                self.status.has(Effects.Burning) or
                self.status.has(Effects.Terror)):
            return

        self.hit_points.increment(amount)

    def effects(self) -> None:
        """
        Handles the effects.
        """

        def effect_callback(effect: Effects):
            if effect == Effects.Freezing:
                self.handle_cold_damage()
            elif effect == Effects.Burning:
                self.handle_burning_damage()

        self.status.for_each_effect(effect_callback)

    def find_adjacent_tile(self) -> Dict[str, int]:
        """
        Finds an adjacent tile.
        """
        # TODO: Implement world.map references
        # if not self.world.map.is_colliding(self.x + 1, self.y):
        #     self.set_position(self.x + 1, self.y)
        # ...
        return {"x": -1, "y": -1}

    def stop(self) -> None:
        """
        Stops the character.
        """
        self.stop_intervals()

    def hit(self, damage: int, attacker: Optional["Character"] = None, aoe: int = 0, is_thorns: bool = False) -> None:
        """
        Handles the hit.
        """
        # Stop hitting if entity is dead.
        if self.is_dead() or self.status.has(Effects.Invincible):
            return

        # Add an entry to the damage table.
        if attacker and attacker.is_player():
            self.add_to_damage_table(attacker, damage)

        # Decrement health by the damage amount.
        self.hit_points.decrement(damage)

        # If this is an AoE attack, we will damage all nearby characters.
        if aoe:
            self.handle_aoe(damage, attacker, aoe)

        # Hit callback on each hit.
        if self.hit_callback:
            self.hit_callback(damage, attacker, is_thorns)

        # If the character has bloodsucking, we let the handler take care of it.
        if attacker and attacker.has_bloodsucking():
            self.handle_bloodsucking(attacker, damage)

        # Call the death callback if the character reaches 0 hitpoints.
        if self.is_dead():
            # Clear the status effects.
            self.status.clear()

            if self.death_callback:
                self.death_callback(attacker)
            return

        # Poison only occurs when we land a hit and attacker has a poisonous weapon.
        if attacker and attacker.is_poisonous() and damage > 0:
            self.handle_poison_damage(attacker)

    def follow(self, target: Optional["Character"] = None) -> None:
        """
        Follows the target.
        """
        # If the character is stunned, we stop.
        if self.is_stunned():
            return

        # If no target is specified and we don't have a target, we stop.
        if not target and not self.has_target():
            return

        target_instance = ""
        if target:
            target_instance = target.instance
        elif self.target:
            target_instance = self.target.instance
        else:
            return
        self.send_to_regions(
            MovementPacket(
                Opcodes.Movement.Follow,
                MovementPacketData(
                    instance=self.instance,
                    target=target_instance
                )
            )
        )

    async def teleport(self, x: int, y: int, with_animation: bool = False) -> None:
        """
        Teleports the character.
        """
        self.set_position(x, y, True)

        self.send_to_regions(
            TeleportPacket(
                TeleportPacketData(
                    instance=self.instance,
                    x=x,
                    y=y,
                    with_animation=with_animation
                )
            )
        )

        await asyncio.sleep(0.5)
        self.teleporting = False

    def countdown(self, time_val: int) -> None:
        """
        Handles the countdown.
        """
        self.send_to_regions(
            CountdownPacket(
                CountdownPacketData(
                    instance=self.instance,
                    time=time_val
                )
            )
        )

    def stop_movement(self) -> None:
        """
        Stops the character's movement.
        """
        self.send_to_regions(
            MovementPacket(
                Opcodes.Movement.Stop,
                MovementPacketData(instance=self.instance)
            )
        )

    def clear_target(self) -> None:
        """
        Clears the target.
        """
        self.target = None

    def clear_attackers(self) -> None:
        """
        Clears the attackers.
        """
        self.attackers = []

    def remove_attacker(self, attacker: "Character") -> None:
        """
        Removes an attacker.
        """
        self.attackers = [a for a in self.attackers if a.instance != attacker.instance]

    def get_attacker_count(self) -> int:
        """
        Gets the attacker count.
        """
        return len(self.attackers)

    def get_attack_rate(self) -> int:
        """
        Gets the attack rate.
        """
        return self.attack_rate

    def get_attack_stats(self) -> Stats:
        """
        Gets the attack stats.
        """
        return Utils.get_empty_stats()

    def get_defense_stats(self) -> Stats:
        """
        Gets the defense stats.
        """
        return Utils.get_empty_stats()

    def get_bonuses(self) -> Bonuses:
        """
        Gets the bonuses.
        """
        return Utils.get_empty_bonuses()

    def get_accuracy_bonus(self) -> int:
        """
        Gets the accuracy bonus.
        """
        return self.get_bonuses().accuracy

    def get_accuracy_level(self) -> int:
        """
        Gets the accuracy level.
        """
        return 1

    def get_strength_level(self) -> int:
        """
        Gets the strength level.
        """
        return 1

    def get_archery_level(self) -> int:
        """
        Gets the archery level.
        """
        return 1

    def get_defense_level(self) -> int:
        """
        Gets the defense level.
        """
        return 1

    def get_damage_bonus(self) -> int:
        """
        Gets the damage bonus.
        """
        return self.get_bonuses().archery if self.is_ranged() else self.get_bonuses().strength

    def get_skill_damage_level(self) -> int:
        """
        Gets the skill damage level.
        """
        return self.get_archery_level() if self.is_ranged() else self.get_strength_level()

    def get_damage_reduction(self) -> int:
        """
        Gets the damage reduction.
        """
        return 1

    def get_attack_style(self) -> AttackStyle:
        """
        Gets the attack style.
        """
        return AttackStyle.None_

    def get_damage_type(self) -> Hits:
        """
        Gets the damage type.
        """
        return self.damage_type

    def get_poison_chance(self) -> int:
        """
        Gets the poison chance.
        """
        return Defaults.POISON_CHANCE

    def get_random_attacker(self) -> Optional["Character"]:
        """
        Gets a random attacker.
        """
        if not self.attackers:
            return None
        # TODO: There should be a function in the random package to return a random element from a list already
        return self.attackers[random.randint(0, len(self.attackers) - 1)]

    def get_aoe(self) -> int:
        """
        AoE damage works on a toggle basis. When a character uses an AoE attack
        it automatically resets the ability to use AoE attacks until it is toggled
        again. Toggling refers to the AoE radius value being set to anything greater
        than 0.
        :returns: The current AoE radius value.
        """
        aoe_val = self.aoe
        if self.aoe:
            self.aoe = 0
        return aoe_val

    def get_projectile_name(self) -> str:
        """
        Gets the projectile name.
        """
        return self.projectile_name

    def get_last_attack(self) -> int:
        """
        Returns the time differential for when the last attack was made.
        """
        # TODO: Implement combat.last_attack reference
        # return int(time.time() * 1000) - self.combat.last_attack
        return 0

    def get_bloodsucking_level(self) -> int:
        """
        Default implementation for bloodsucking level, defaults to 1 for all characters.
        """
        return 1

    def has_special_attack(self) -> bool:
        """
        Default implementation for checking if the character has a special attack.
        """
        return False

    def has_target(self) -> bool:
        """
        Checks if the character has a target.
        """
        return self.target is not None

    def has_attacker(self, attacker: "Character") -> bool:
        """
        Checks if the character has an attacker.
        """
        return any(a.instance == attacker.instance for a in self.attackers)

    def has_arrows(self) -> bool:
        """
        Default implementation for checking if the character has arrows.
        """
        return True

    def has_bloodsucking(self) -> bool:
        """
        Default implementation for checking if the character has the bloodsucking ability.
        """
        return False

    def in_combat(self) -> bool:
        """
        Checks if the character is in combat.
        """
        # TODO: Implement combat started and expired check
        # return (self.combat.started or
        #         len(self.attackers) > 0 or
        #         self.has_target() or
        #         not self.combat.expired())
        return len(self.attackers) > 0 or self.has_target()

    def is_ranged(self) -> bool:
        """
        `is_ranged` is a general function that checks if the character is using
        any form of ranged attack. This can be either a bow or magic spells.
        """
        return self.attack_range > 1

    def is_archer(self) -> bool:
        """
        Checks if the character is an archer.
        """
        return self.is_ranged() and not self.is_magic()

    def is_magic(self) -> bool:
        """
        Default implementation for checking if the character is magic.
        """
        return False

    def is_dead(self) -> bool:
        """
        Checks if the character is dead.
        """
        return self.hit_points.is_empty() or self.dead

    def is_near_target(self) -> bool:
        """
        Checks if the character is within its own attack range next to its target.
        """
        if not self.target:
            return False

        if self.is_ranged():
            return (self.get_distance(self.target) <= self.attack_range and
                    self.plateau_level >= self.target.plateau_level)

        return self.is_adjacent(self.target)

    def is_poisonous(self) -> bool:
        """
        Default implementation to check if the character is poisonous.
        """
        return False

    def is_on_same_tile(self) -> bool:
        """
        Checks if the character's target is on the same tile as the character.
        """
        if not self.target:
            return False
        return self.x == self.target.x and self.y == self.target.y

    def is_stunned(self) -> bool:
        """
        Indicates whether or not the character is able to move.
        """
        return self.status.has(Effects.Stun)

    def can_attack(self, target: "Character") -> bool:
        """
        Checks if the character can attack the target.
        """
        if target.is_pet():
            # TODO: Implement notify()
            # if self.is_player():
            #     self.notify('misc:CANNOT_ATTACK_PET')
            return False

        if target.is_mob():
            # TODO: Implement Player/Quests/Tutorial specific logic
            # if self.is_player() and not self.quests.can_attack_in_tutorial():
            #     self.notify('misc:CANNOT_ATTACK_MOB')
            #     return False
            return True

        if not self.is_player() or not target.is_player():
            return False

        # TODO: Implement more player specific checks (Cheater, Minigame, PvP Area, Level Difference)
        return True

    @override
    def set_position(self, x: int, y: int, with_teleport: bool = False) -> None:
        """
        Override of the superclass `set_position`. Since characters are the only
        instances capable of movement, we need to update their position in the grids.
        We also add a teleport flag that we can use to prevent the character from
        performing actions during the teleportation process.
        :param x: The new x grid position.
        :param y: The new y grid position.
        :param with_teleport: Whether the character is teleporting or not.
        """
        if self.teleporting:
            return

        super().set_position(x, y)

        # TODO: Implement world.map references
        # self.world.map.grids.update_entity(self)

        if with_teleport:
            self.teleporting = True

    def set_target(self, target: "Character") -> None:
        """
        Sets the new target.
        """
        self.target = target

    def add_attacker(self, attacker: "Character") -> None:
        """
        Adds an attacker to our list of attackers.
        """
        if attacker.instance == self.instance or self.has_attacker(attacker):
            return
        self.attackers.append(attacker)

    def add_to_damage_table(self, attacker: "Character", damage: int) -> None:
        """
        Adds or creates an entry in the damage table for the attacker.
        """
        if damage >= self.hit_points.get_hit_points():
            damage = self.hit_points.get_hit_points()

        if attacker.instance not in self.damage_table:
            self.damage_table[attacker.instance] = damage
        else:
            self.damage_table[attacker.instance] += damage

    def add_status_effect(self, hit: Hit) -> None:
        """
        Adds a status effect to the character based on the hit type.
        """
        if self.is_dead() or hit.type == Hits.Normal:
            return

        if hit.type == Hits.Stun:
            self.status.add_with_timeout(Effects.Stun, Constants.STUN_DURATION)
        elif hit.type == Hits.Terror:
            self.status.add_with_timeout(Effects.Terror, Constants.TERROR_DURATION)
        elif hit.type == Hits.Freezing:
            if not self.status.has(Effects.SnowPotion):
                self.status.add_with_timeout(Effects.Freezing, Constants.FREEZING_DURATION)
        elif hit.type == Hits.Burning:
            if not self.status.has(Effects.FirePotion):
                self.status.add_with_timeout(Effects.Burning, Constants.BURNING_DURATION)

    def find_nearest_target(self) -> Optional["Character"]:
        """
        Finds the nearest character to target within the list of attackers.
        """
        if not self.attackers:
            return None

        nearest = self.attackers[0]
        min_dist = self.get_distance(nearest)

        for i in range(1, len(self.attackers)):
            dist = self.get_distance(self.attackers[i])
            if dist < min_dist:
                min_dist = dist
                nearest = self.attackers[i]

        return nearest

    def set_hit_points(self, hit_points: int) -> None:
        """
        Sets the hit points.
        """
        self.hit_points.set_hit_points(hit_points)

    def set_poison(self, type_val: Optional[PoisonTypes] = None, start: Optional[datetime] = None) -> None:
        """
        Sets the poison status and makes a callback. If
        no type is specified, we remove the poison.
        :param type_val: The type of poison we are adding.
        :param start: Optional parameter for setting when poison starts (for loading from database).
        """
        remove = type_val is None

        if remove and not self.poison:
            return

        exists = type_val is not None and self.poison is not None

        if type_val is not None:
            self.poison = Poison(PoisonTypes(type_val), start)
        else:
            self.poison = None

        if remove:
            self.stop_poison_interval()
        elif not exists:
            self.start_poison_interval()

        if self.poison_callback:
            self.poison_callback(type_val, not exists)

    def set_orientation(self, orientation: Orientation) -> None:
        """
        Sets the orientation.
        """
        self.orientation = orientation

    def send_to_region(self, packet: Packet, ignore: bool = False) -> None:
        """
        Sends a packet to the current region.
        """
        self.world.push(PacketType.Region, PacketData(
            region=self.region,
            packet=packet,
            ignore=self.instance if ignore else ''
        ))

    def send_to_regions(self, packet: Packet, ignore: bool = False) -> None:
        """
        Sends a packet to all regions surrounding the player.
        """
        self.world.push(PacketType.Regions, PacketData(
            region=self.region,
            packet=packet,
            ignore=self.instance if ignore else ''
        ))

    def send_broadcast(self, packet: Packet) -> None:
        """
        Broadcasts a message to all the players in the world.
        """
        self.world.push(PacketType.Broadcast, PacketData(
            packet=packet
        ))

    def for_each_nearby_character(self, callback: Callable[["Character"], None], range_val: int = 1) -> None:
        """
        Iterates through each nearby character.
        """
        # TODO: Implement world.get_grids() reference
        pass

    def for_each_attacker(self, callback: Callable[["Character"], None]) -> None:
        """
        Iterates through each attacker.
        """
        for attacker in self.attackers:
            callback(attacker)

    @override
    @abstractmethod
    def serialize(self) -> EntityData:
        """
        Serializes the character.
        """
        data = super().serialize()
        data.movement_speed = self.movement_speed
        data.orientation = self.orientation
        return data

    def on_poison(self, callback: PoisonCallback) -> None:
        """
        Callback for when the character is poisoned.
        """
        self.poison_callback = callback

    def on_hit(self, callback: HitCallback) -> None:
        """
        Callback for when the character is hit.
        """
        self.hit_callback = callback

    def on_death(self, callback: DeathCallback) -> None:
        """
        Callback for when the character dies.
        """
        self.death_callback = callback

    def on_death_impl(self, callback: DeathCallback) -> None:
        """
        Implementation for the death callback.
        """
        self.death_i_callback = callback
