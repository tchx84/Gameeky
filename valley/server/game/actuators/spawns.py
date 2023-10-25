from .base import Actuator as BaseActuator

from ....common.utils import get_time_milliseconds


class Actuator(BaseActuator):
    name = "spawns"
    interactable = False

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self._timestamp = get_time_milliseconds()

    def tick(self) -> None:
        timestamp = get_time_milliseconds()

        if (timestamp - self._timestamp) / 1000 < self._entity.rate:
            return

        self._entity.spawn()
        self._timestamp = timestamp

        super().tick()
