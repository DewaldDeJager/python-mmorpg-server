import random

from network.modules import EntityType
from network.shared_types import Bonuses, Stats


class Utils:
    _counter = -1

    @classmethod
    def create_instance(cls, identifier: EntityType) -> str:
        """
        Takes the type of entity and creates a UNIQUE instance id.
        :param identifier: The type of entity.
        :return: A randomly generated string.
        """
        cls._counter += 1
        return f"{identifier.value}-{random.randint(1000, 100_000)}{cls._counter}"

    @classmethod
    def get_guest_username(cls) -> str:
        username = f"guest{cls._counter}"
        cls._counter += 1
        return username

    @staticmethod
    def get_empty_stats() -> Stats:
        """
        For the purpose of not repeatedly writing the same stats.
        :return: Empty stats values.
        """
        return Stats(crush=0, slash=0, stab=0, archery=0, magic=0)

    @staticmethod
    def get_empty_bonuses() -> Bonuses:
        """
        Creates an empty bonuses object.
        :return: Empty bonuses object with default values.
        """
        return Bonuses(accuracy=0, strength=0, archery=0, magic=0)

    @staticmethod
    def random_weighted_int(min_val: int, max_val: int, weight: float) -> int:
        """
        Creates a distribution based on weight. Instead of having an equal chance
        of picking out a number between min and max, we can have a higher chance
        of either numbers depending on the weight. Lower weight means more likely
        to pick numbers closer to maximum, and vice versa.
        :param min_val: Minimum number (inclusive)
        :param max_val: Maximum number (inclusive)
        :param weight: 0-infinity, closer to 0 higher chance of picking maximum.
        :return: Random integer with weight between min and max.
        """
        return int((random.random() ** weight) * (max_val - min_val + 1) + min_val)

utils = Utils()
