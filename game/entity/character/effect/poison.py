from datetime import datetime, timedelta
from network.modules import PoisonTypes, PoisonData

class Poison:
    """
    Initializes an object of poison that can be stored in a character.
    """
    def __init__(self, poison_type: PoisonTypes, start: datetime | None = None):
        self.type = poison_type
        self.start = start or datetime.now()

        poison_info = PoisonData[self.type]
        self.name = poison_info.name
        self.damage = int(poison_info.damage)
        # Convert seconds from PoisonData to timedelta
        self.duration = timedelta(seconds=poison_info.duration) if poison_info.duration != -1 else timedelta(seconds=-1)
        self.rate = timedelta(seconds=poison_info.rate)

    def expired(self) -> bool:
        """
        Checks if the poison status has expired. A poison with the duration of
        -1 will never expire until it is cured.
        @returns If the time difference between when poison started and now is
        greater than the duration of the poison.
        """
        if self.duration.total_seconds() < 0:
            return False

        return (datetime.now() - self.start) >= self.duration

    def get_remaining_time(self) -> float:
        """
        @returns The remaining amount of time in the poison effect in milliseconds. 
        Used for loading once the player logs back in to the game.
        """
        if self.duration.total_seconds() < 0:
            return -1.0
            
        elapsed = datetime.now() - self.start
        remaining = self.duration - elapsed
        return max(0.0, remaining.total_seconds() * 1000)
