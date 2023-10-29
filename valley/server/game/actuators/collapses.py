from .base import Actuator as BaseActuator

from ..definitions import Delay

from ....common.definitions import Action


class Actuator(BaseActuator):
    name = "collapses"
    interactable = False
    activatable = False

    def tick(self) -> None:
        if self._seconds_since_activation() <= Delay.MAX:
            return

        if not self._entity.surroundings:
            return

        self._entity.stop()
        self._entity.perform(Action.DESTROY)
