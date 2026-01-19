from typing import Callable, Optional
from game.entity.character.points.points import Points

# Type alias for better readability
ManaCallback = Callable[[], None]


class Mana(Points):
    def __init__(self, mana: int, max_mana: int | None = None):
        super().__init__(mana, max_mana if max_mana is not None else mana)
        self.mana_callback: Optional[ManaCallback] = None

    def increment(self, amount: int) -> None:
        super().increment(amount)

        if self.mana_callback:
            self.mana_callback()

    def decrement(self, amount: int) -> None:
        super().decrement(amount)

        if self.mana_callback:
            self.mana_callback()

    def update_mana(self, mana: int, max_mana: int | None = None) -> None:
        super().update_points(mana, max_mana)

    def set_points(self, points: int) -> None:
        super().set_points(points)

        if self.mana_callback:
            self.mana_callback()

    def set_mana(self, mana: int) -> None:
        self.set_points(mana)

    def set_max_mana(self, max_mana: int) -> None:
        super().set_max_points(max_mana)

    def get_mana(self) -> int:
        return self.points

    def get_max_mana(self) -> int:
        return self.max_points

    def on_mana(self, callback: ManaCallback) -> None:
        self.mana_callback = callback
