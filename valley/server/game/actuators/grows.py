from .base import Actuator as BaseActuator

from ....common.state import State
from ....common.utils import get_time_milliseconds


class Actuator(BaseActuator):
    name = "grows"
    interactable = False

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self._timestamp = get_time_milliseconds()

    def tick(self) -> None:
        timestamp = get_time_milliseconds()

        if (timestamp - self._timestamp) / 1000 < self._entity.rate:
            return

        self._entity.state = State.DESTROYED
        self._entity.spawn()

        super().tick()
