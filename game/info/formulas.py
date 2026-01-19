import math
import random
from typing import List, Optional, Union

from common.utils import Utils
from network.modules import AttackStyle, Constants, DamageStyle, Effects
from network.shared_types import Stats


class Formulas:
    LEVEL_EXP: List[int] = []

    @staticmethod
    def get_damage(attacker, target, critical: bool = False) -> int:
        """
        Damage is calculated by taking into consideration the attacker's accuracy
        level and bonus. We then use the `random_weighted_int` to create a weighted distribution
        for the likelihood of attaining maximum damage. The maximum attainable accuracy is
        dictated by the constant MAX_ACCURACY. The higher the accuracy value the less likely to achieve
        maximum damage in a hit. We `add` onto the max accuracy such that
        the higher the level the lower the addition. The higher the accuracy, the lower the chance
        of hitting max damage.

        Max hit chance based on accuracy:
        > 0.45 - 2.19%
        > 0.90 - 0.94%
        > 1.35 - 0.71%
        > 2.50 -> 0.48%
        """
        accuracy_bonus = attacker.get_accuracy_bonus()
        accuracy_level = attacker.get_accuracy_level()
        accuracy_modifier = Formulas.get_accuracy_weight(attacker, target)
        defense_level = target.get_defense_level()
        max_damage = Formulas.get_max_damage(attacker, critical)
        accuracy: float = Constants.MAX_ACCURACY

        # The damage output is calculated by taking the attacker's maximum damage output
        # and comparing against the accuracy calculated relative to the target's stats,
        # defense level, as well as the attacker's accuracy level, bonus, and stats.
        # We use four modifiers to output the final damage, and a weighted randomInt
        # distribution (think graphs skewed to the right or left depending on the accuracy).
        # The maximum damage takes in consideration tha player's strength level, their
        # weapon bonuses, (or their magic/archery if that's what they're using).
        #
        # The accuracy works backwards, 0.45 being the most accurate, and any number heigher
        # skews the graph towards the lower-end (higher likelihood of hitting lower damage).
        #
        # The accuracy consists of four parts, the accuracy bonus, the accuracy level,
        # the defense level of the target, and the accuracy modifier.
        #
        # The accuracy bonus is the bonus given by the attacker's equipment. We picked a maximum
        # of 55 since that is currently the maximum acquirable bonus from equipments the best
        # equipments. It's a linear scaling from 0-1, with highest bonus giving us the highest
        # accuracy. Note that this is subject to changes in the nearby future, and we do not
        # intend to keep it entirely linear.
        #
        # The next is the linear scaling of the accuracy level against the maximum level. The
        # higher your accuracy level, the higher the accuracy. This modifier has an absolute lowest
        # value of 0.01 (most accurate at maximum level) and highest value of 1.35
        # (lowest accuracy at level 1 accuracy).
        #
        # The next is a linear scale of the target's defense level. The higher their defense level the
        # more it will affect our accuracy. The way this was calculated was by considering the maximum
        # level a player will be able to reach (135). If we attack a player with maximum defense, our
        # accuracy will be throttled by 1.015. If we attack a player with level 1 defense, our accuracy
        # will be affected by 0.0075 (giving us more accuracy).
        #
        # Lastly this is the accuracy modifier of the attack stats. The attack stats are compared against
        # the target's defense stats and take into considering the primary attack style of the attacker
        # versus the primary defense style. For example, if we use slash against a target with a high defense
        # in slash, then our accuracy is lower than if we use slash against a target with a low defense in slash.
        # In order to minimize the accuracy of an attacker, your defense style must be the attacker's attack style.
        # If our attack stats are negative due to the target's extremely high defense stats, we append a 1.5
        # reduction in accuracy by default.
        #
        # All of these modifiers added together determine how much we stray away from the highest accuracy - 0.45.

        # Linearly increase accuracy based on accuracy bonus, prevent from going over 50.
        accuracy += 0 if accuracy_bonus > 70 else 1 - accuracy_bonus / 70

        # Append the accuracy level bonus, we use a 1.75 modifier since skill level matters more.
        accuracy += (Constants.MAX_LEVEL - accuracy_level + 1) * 0.01

        # Append the defense level of the target to the accuracy modifier.
        accuracy += defense_level * 0.0175

        # We use the scalar difference of the stats to append onto the accuracy.
        accuracy += 1.5 if accuracy_modifier < 0 else -(math.sqrt(accuracy_modifier) / 22.36) + 1

        # Critical damage boosts accuracy by a factor of 0.15;
        if critical:
            accuracy -= 0.15

        # Apply the attack style modifiers.
        attack_style = attacker.get_attack_style()
        if attack_style in (AttackStyle.Fast, AttackStyle.LongRange):
            # Rapid attack style decreases accuracy by a factor of 0.05;
            accuracy += 0.05
        elif attack_style in (AttackStyle.Stab, AttackStyle.Focused, AttackStyle.Accurate):
            # Rapid attack style increases accuracy by a factor of 0.11;
            accuracy -= 0.11
        elif attack_style in (AttackStyle.Crush, AttackStyle.Chop):
            # Rapid attack style increases accuracy by a factor of 0.07
            accuracy -= 0.07
        elif attack_style == AttackStyle.Shared:
            # Shared attack style increases accuracy by a factor of 0.05
            accuracy -= 0.05

        # Increase accuracy if the attacker has the accuracy potion effect.
        if attacker.status.has(Effects.AccuracyBuff):
            accuracy -= 0.07
        if attacker.status.has(Effects.AccuracySuperBuff):
            accuracy -= 0.12

        # Decrease accuracy if the target has the defense potion effect.
        if target.status.has(Effects.DefenseBuff):
            accuracy += 0.08
        if target.status.has(Effects.DefenseSuperBuff):
            accuracy += 0.12

        # Increase accuracy if the target has the terror effect.
        if target.status.has(Effects.Terror):
            accuracy -= 0.4

        # Terror decreases overall accuracy, so we increase it by 1.
        if attacker.status.has(Effects.Terror):
            accuracy += 1

        # We apply the damage absorption onto the max damage. See `get_damage_reduction` for more information.
        max_damage *= target.get_damage_reduction()

        # We use the weighted randomInt distribution to determine the damage.
        random_damage = Utils.random_weighted_int(0, int(max_damage), accuracy)

        # Limit the damage to the target's remaining health.
        if random_damage > target.hit_points.get_hit_points():
            random_damage = target.hit_points.get_hit_points()

        return random_damage

    @staticmethod
    def get_max_damage(character, critical: bool = False) -> float:
        """
        Calculates the maximum damage attainable by a character given their strength (or archery) level,
        their equipment bonuses, and any special active effects.
        :param critical: A critical hit boosts the damage multiplier by 1.5x;
        """
        bonus = character.get_damage_bonus()
        level = character.get_skill_damage_level()
        damage = (bonus + level) * 1.25

        # Apply a 50% max damage boost upon critical damage.
        if critical:
            damage *= 1.5

        # Player characters get a boost of 5 damage.
        if character.is_player():
            damage += 5

        # Different attack styles give different bonuses.
        attack_style = character.get_attack_style()
        if attack_style in (AttackStyle.Focused, AttackStyle.Slash):
            # Focused attack style boosts maximum damage by 10%
            damage *= 1.1
        elif attack_style in (AttackStyle.Crush, AttackStyle.Hack):
            # Crush gives a 5% boost.
            damage *= 1.05
        elif attack_style == AttackStyle.Shared:
            # Shared attack style gives a 3% boost.
            damage *= 1.03

        # Apply a 10% damage boost if the character has the strength potion effect.
        if character.status.has(Effects.StrengthBuff):
            damage *= 1.1

        # Apply 15% damage boost if the character has the super strength potion effect.
        if character.status.has(Effects.StrengthSuperBuff):
            damage *= 1.15

        # Ensure the damage is not negative.
        if damage < 0:
            damage = 0

        return damage

    @staticmethod
    def get_accuracy_weight(attacker, target) -> float:
        """
        Calculates the accuracy modifier for a character given their attack and defense stats.
        The accuracy modifier is used to determine the likelihood of attaining maximum damage
        in a hit. The higher the accuracy modifier, the more likely to attain maximum damage.
        :param attacker: The attacking character.
        :param target: The defending character.
        :returns: A float of the accuracy modifier (to be used for calculating likelihood of attaining max damage).
        """
        attacker_stats = attacker.get_attack_stats()
        target_stats = target.get_defense_stats()
        attack_style = Formulas.get_primary_style(attacker_stats)  # primary attack style of the attacker
        defense_style = Formulas.get_primary_style(target_stats)  # primary defense style of the target

        weights = {
            "crush": (attacker_stats.crush - target_stats.crush) / 3,
            "slash": (attacker_stats.slash - target_stats.slash) / 3,
            "stab": (attacker_stats.stab - target_stats.stab) / 3,
            "magic": (attacker_stats.magic - target_stats.magic) / 3,
            "archery": (attacker_stats.archery - target_stats.archery) / 3
        }

        total_weight = sum(w for w in weights.values() if w >= 0)

        # Respective classes use their own weights.
        if attacker.is_archer():
            total_weight = weights["archery"]
        if attacker.is_magic():
            total_weight = weights["magic"]

        # If our attack style is the same or none then we do not have any advantage in our accuracy.
        if attack_style == defense_style or attack_style == DamageStyle.None_:
            return total_weight or 1.0

        # If we have a attack style against a defense style that is not the same, then we can
        # remove the 1/3th of the weight and append the full weight of the attack style to the
        # accuracy modifier.

        if attack_style == DamageStyle.Crush:
            total_weight += weights["crush"] if defense_style == DamageStyle.Slash else -weights["crush"] / 2
        elif attack_style == DamageStyle.Slash:
            total_weight += weights["slash"] if defense_style == DamageStyle.Stab else -weights["slash"] / 2
        elif attack_style == DamageStyle.Stab:
            total_weight += weights["stab"] if defense_style == DamageStyle.Crush else -weights["stab"] / 2
        elif attack_style == DamageStyle.Magic:
            total_weight += weights["magic"]
        elif attack_style == DamageStyle.Archery:
            total_weight += weights["archery"]

        # Ensure the weight is always positive and more than 1 for the sake of combat mechanics
        return max(total_weight, 1.0)

    @staticmethod
    def get_primary_style(stats: Stats) -> DamageStyle:
        """
        Compares every attack stat against every other attack stat and extracts which attack
        stat is the greatest. This gives us tth primary attack style of the charater based
        on their overall stats
        :param stats: The stats object to look through (either attack or defense).
        :returns: The primary style of attack.
        """
        if (stats.crush > stats.slash and stats.crush > stats.stab and
                stats.crush > stats.magic and stats.crush > stats.archery):
            return DamageStyle.Crush
        if (stats.slash > stats.crush and stats.slash > stats.stab and
                stats.slash > stats.magic and stats.slash > stats.archery):
            return DamageStyle.Slash
        if (stats.stab > stats.crush and stats.stab > stats.slash and
                stats.stab > stats.magic and stats.stab > stats.archery):
            return DamageStyle.Stab
        if (stats.magic > stats.crush and stats.magic > stats.slash and
                stats.magic > stats.stab and stats.magic > stats.archery):
            return DamageStyle.Magic
        if (stats.archery > stats.crush and stats.archery > stats.slash and
                stats.archery > stats.stab and stats.archery > stats.magic):
            return DamageStyle.Archery

        return DamageStyle.None_

    @staticmethod
    def get_weapon_break(attacker, target) -> Optional[bool]:
        if not attacker or not target:
            return None

        # The chance a weapon will break ....
        break_chance = random.uniform(1, 100)
        return break_chance > 75

    @staticmethod
    def next_exp(experience: int) -> int:
        if experience < 0:
            return -1

        for i in range(1, len(Formulas.LEVEL_EXP)):
            if experience < Formulas.LEVEL_EXP[i]:
                return Formulas.LEVEL_EXP[i]

        return -1

    @staticmethod
    def prev_exp(experience: int) -> int:
        if experience < 0:
            return 0

        for i in range(Constants.MAX_LEVEL, 0, -1):
            if i < len(Formulas.LEVEL_EXP) and experience >= Formulas.LEVEL_EXP[i]:
                return Formulas.LEVEL_EXP[i]

        return 0

    @staticmethod
    def exp_to_level(experience: int) -> int:
        if experience < 0:
            return -1

        for i in range(1, len(Formulas.LEVEL_EXP)):
            if experience < Formulas.LEVEL_EXP[i]:
                return i

        return Constants.MAX_LEVEL

    @staticmethod
    def levels_to_experience(start_level: int, end_level: int) -> int:
        """
        Calculates the experience required to go from one level to another.
        :param start_level: The level we are starting from.
        :param end_level: The level we are ending at.
        """
        return Formulas.LEVEL_EXP[end_level] - Formulas.LEVEL_EXP[start_level]

    @staticmethod
    def get_max_hit_points(level: int) -> int:
        """
        Formula used to calcualte maximum hitpoints.
        :param level: The level of the health skill generally.
        :returns: The maximum hitpoints number value.
        """
        return 39 + level * 30

    @staticmethod
    def get_max_mana(level: int) -> int:
        """
        Obtains the max mana given a level specified.
        :param level: The level we are using to calculate max mana.
        :returns: The max mana number value.
        """
        return 20 + level * 24

    @staticmethod
    def get_poison_chance(level: int) -> int:
        """
        Probability is calculated using the primary skill for dealing damage. For example
        the player's strength if using a sword, or the archery if using a bow. 235 is picked
        such that the maximum attainable poison chance is a random integer between 1 and 100.
        With a poison chance of 10 as specified in Modules, the player has a minimum 6% chance
        of poisoning another character, and a maximum of 15% when the respective skill is maxed.
        :param level: The level of the player.
        """
        # Chance is per 235 - level, each level increases the chance in poisioning.
        return random.randint(0, 235 - level)

    @staticmethod
    def get_effect_chance() -> bool:
        """
        :returns: Whether or not the effect chance was successful.
        """
        return random.randint(0, 100) < 5

    @staticmethod
    def get_enchant_chance(tier: int) -> bool:
        """
        Calculates the chance of an item to be enchanted.
        :param tier: The tier of the shards the player is using.
        """
        return random.randint(0, 100) < 8 * tier
