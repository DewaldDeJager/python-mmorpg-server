import random

from network.modules import EntityType

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

utils = Utils()
