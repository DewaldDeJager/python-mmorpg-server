from typing import Callable, Optional
from game.entity.character.points.points import Points

# Type alias for better readability
HitPointsCallback = Callable[[], None]


class HitPoints(Points):
    def __init__(self, hit_points: int, max_hit_points: int | None = None):
        super().__init__(hit_points, max_hit_points if max_hit_points is not None else hit_points)
        self.hit_points_callback: Optional[HitPointsCallback] = None

    def increment(self, amount: int) -> None:
        super().increment(amount)

        if self.hit_points_callback:
            self.hit_points_callback()

    def decrement(self, amount: int) -> None:
        super().decrement(amount)

        if self.hit_points_callback:
            self.hit_points_callback()

    def update_hit_points(self, hit_points: int, max_hit_points: int | None = None) -> None:
        super().update_points(hit_points, max_hit_points)

    def set_points(self, points: int) -> None:
        super().set_points(points)

        if self.hit_points_callback:
            self.hit_points_callback()

    def set_hit_points(self, hit_points: int) -> None:
        self.set_points(hit_points)

    def set_max_hit_points(self, max_hit_points: int) -> None:
        super().set_max_points(max_hit_points)

    def get_hit_points(self) -> int:
        return self.points

    def get_max_hit_points(self) -> int:
        return self.max_points

    def on_hit_points(self, callback: HitPointsCallback) -> None:
        self.hit_points_callback = callback
