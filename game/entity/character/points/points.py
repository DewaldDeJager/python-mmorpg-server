from abc import ABC


class Points(ABC):
    """
    An abstract class for creating a system used to manage points.
    """

    def __init__(self, points: int, max_points: int):
        self.points = points
        self.max_points = max_points

    def increment(self, amount: int) -> None:
        """
        Increments the points by the specified `amount`.
        @param amount How much to increment the points by.
        """
        self.set_points(self.points + amount)

    def decrement(self, amount: int) -> None:
        """
        Decrements the points by the specified `amount`.
        @param amount How much to decrement the points by.
        """
        self.set_points(self.points - amount)

    def update_points(self, points: int, max_points: int | None = None) -> None:
        """
        Updates the points based on the specified `info`.
        @param points The hit points to set.
        @param max_points The maximum hit points to set.
        """
        if max_points is None:
            max_points = points

        self.set_max_points(max_points)
        self.set_points(points)

    def set_points(self, points: int) -> None:
        """
        Sets the points to the specified `points`.
        @param points The value to set to.
        """
        self.points = points

        if self.points >= self.max_points:
            self.points = self.max_points

        if self.points < 0:
            self.points = 0

    def set_max_points(self, max_points: int) -> None:
        """
        Sets the maximum points to the specified `max_points`.
        @param max_points The value to set to.
        """
        if self.points > max_points:
            self.points = max_points

        self.max_points = max_points

    def reset(self) -> None:
        """
        Resets the current points to the maximum points.
        """
        self.set_points(self.max_points)

    def is_full(self) -> bool:
        """
        Returns whether or not the points are at the maximum points.
        @returns `True` if the points are at the maximum points.
        """
        return self.points >= self.max_points

    def is_empty(self) -> bool:
        """
        Returns whether or not the points are empty.
        @returns `True` if there are no points.
        """
        return self.points <= 0

    def serialize(self) -> list[int]:
        """
        @returns A serialized version of the points.
        """
        return [self.points, self.max_points]
