from .base import Actuator as BaseActuator

from ....common.definitions import Action
from ....common.utils import get_time_milliseconds


class Actuator(BaseActuator):
    name = "collapses_t"
    interactable = False
    activatable = False

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self._timestamp = get_time_milliseconds()

    def tick(self) -> None:
        if (get_time_milliseconds() - self._timestamp) / 1000 <= self._entity.rate:
            return

        self._entity.stop()
        self._entity.perform(Action.DESTROY)
