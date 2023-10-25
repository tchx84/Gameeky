from .base import Actuator as BaseActuator

from ..definitions import Recovery

from ....common.utils import get_time_milliseconds


class Actuator(BaseActuator):
    name = "deteriorates"
    interactable = False
    activatable = False

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self._max_durability = self._entity.durability
        self._timestamp_tick = get_time_milliseconds()

    def tick(self) -> None:
        timestamp = get_time_milliseconds()
        seconds_since_tick = (timestamp - self._timestamp_tick) / 1000
        self._timestamp_tick = timestamp

        self._entity.durability -= (
            self._max_durability
            * (Recovery.MAX - self._entity.recovery)
            * seconds_since_tick
        )
