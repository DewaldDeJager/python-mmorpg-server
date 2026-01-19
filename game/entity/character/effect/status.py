import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Callable, Optional
from network.modules import Effects
from database.models.player import SerializedEffects, SerializedDuration


class Duration:
    def __init__(self, task: asyncio.Task, start_time: datetime, duration: timedelta):
        self.task = task
        self.start_time = start_time
        self.duration = duration


class Status:
    def __init__(self):
        self.effects: List[Effects] = []
        self.durations: Dict[Effects, Duration] = {}
        self.add_callback: Optional[Callable[[Effects], None]] = None
        self.remove_callback: Optional[Callable[[Effects], None]] = None

    def load(self, effects: SerializedEffects) -> None:
        """
        Loads the serialized status effects from the database and uses the start time
        relative to the duration of the effect to reinstantiate it if applicable. We use
        the calculated remaining time upon logging out to determine how long to set the
        timeout for.
        :param effects: The list of serialized status effects from the database.
        """
        for effect_id, effect in effects.items():
            # Effect has already passed our current time, just ignore it.
            if effect.remaining_time < 100:
                continue

            self.add_with_timeout(Effects(effect_id), effect.remaining_time)

    def add(self, *status_effects: Effects) -> None:
        """
        Adds a status effect to the character's list of effects if it has not
        already been added. Effects can only be applied once.
        :param status_effects: The new status(es) effect we are adding.
        """
        for status in status_effects:
            # Don't add the effect if it already exists.
            if self.has(status):
                continue

            self.effects.append(status)

            if self.add_callback:
                self.add_callback(status)

    def add_with_timeout(
            self,
            status_effect: Effects,
            duration_ms: int,
            callback: Optional[Callable[[], None]] = None
    ) -> None:
        """
        Adds a status effect to the character's list and sets a timeout with the specified
        duration. Once the timeout is up, the status effect will be removed and the callback
        function is executed.
        :param status_effect: The status effect we are adding.
        :param duration_ms: Duration until the timeout is up in milliseconds.
        :param callback: The callback function to execute once the timeout is up.
        """
        # A temporary freezing effect cannot be added if the player has a permanent one.
        if status_effect == Effects.Freezing and self.has_permanent_freezing():
            return

        self.add(status_effect)

        # Clear existing timeouts.
        if status_effect in self.durations:
            self.durations[status_effect].task.cancel()
            del self.durations[status_effect]

        # Start a new effect duration handler.
        async def timeout_coro():
            try:
                await asyncio.sleep(duration_ms / 1000.0)
                self.remove(status_effect)
                if callback:
                    callback()
            except asyncio.CancelledError:
                # Task was cancelled, don't remove or call callback
                pass

        task = asyncio.create_task(timeout_coro())

        self.durations[status_effect] = Duration(
            task=task,
            start_time=datetime.now() - timedelta(seconds=1),  # Match TS: Date.now() - 1000
            duration=timedelta(milliseconds=duration_ms)
        )

    def remove(self, *status_effects: Effects) -> None:
        """
        Removes one or more status effects from the character's list of effects.
        :param status_effects: The status effect(s) we are removing.
        """
        for status in status_effects:
            if status in self.effects:
                self.effects.remove(status)

            # Remove the status effect from the list of durations.
            if status in self.durations:
                self.durations[status].task.cancel()
                del self.durations[status]

            if self.remove_callback:
                self.remove_callback(status)

    def clear(self) -> None:
        """
        Removes all the effects and timeouts from the character's list of effects.
        """
        self.effects = []

        # Clear all the timeouts.
        for status in list(self.durations.keys()):
            self.durations[status].task.cancel()
            del self.durations[status]

    def has(self, status: Effects) -> bool:
        """
        Checks the array of status effects to see if the character has the status effect.
        :param status: The status effect we are checking the existence of.
        :returns: Whether or not the character has the status effect in the array of effects.
        """
        return status in self.effects

    def has_timeout(self, status: Effects) -> bool:
        """
        Checks whether or not the character has a status effect with a timeout.
        :param status: The status effect we are checking the existence of.
        :returns: Whether or not there is an existent timeout for the status effect.
        """
        return status in self.durations

    def has_permanent_freezing(self) -> bool:
        """
        Permanent freezing is applied when in an area with freezing effect. This one does not
        have a timeout and can only be removed by leaving the area (or temporarily prevented
        by using a snow potion).
        :returns: Whether we have the freezing effect and no timeout associated with it.
        """
        return self.has(Effects.Freezing) and not self.has_timeout(Effects.Freezing)

    def serialize(self) -> SerializedEffects:
        """
        Serializes the status effects for storing them into the database.
        This is to prevent people from logging out and back in to remove
        the status effects.
        :returns: A serialized effects object containing all the currently active durations.
        """
        effects: SerializedEffects = {}

        now = datetime.now()
        for status, duration in self.durations.items():
            # Calculate remaining time in milliseconds
            elapsed = now - duration.start_time
            remaining = duration.duration - elapsed
            remaining_ms = int(max(0, int(remaining.total_seconds() * 1000)))

            effects[int(status)] = SerializedDuration(remaining_time=remaining_ms)

        return effects

    def for_each_effect(self, callback: Callable[[Effects], None]) -> None:
        """
        Iterates through all the active status effects and executes the callback function.
        :param callback: Contains the status effect we are iterating through currently.
        """
        for status in self.effects:
            callback(status)

    def on_add(self, callback: Callable[[Effects], None]) -> None:
        """
        Callback for when a status effect is added onto the player.
        :param callback: The status effect we are adding.
        """
        self.add_callback = callback

    def on_remove(self, callback: Callable[[Effects], None]) -> None:
        """
        Callback for when a status effect is removed from the player.
        :param callback: The status effect we are removing.
        """
        self.remove_callback = callback
