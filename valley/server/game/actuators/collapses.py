from .base import Actuator as BaseActuator

from ....common.definitions import Action


class Actuator(BaseActuator):
    name = "collapses"
    interactable = False
    activatable = False

    def tick(self) -> None:
        if self._seconds_since_activation() <= self._entity.rate:
            return

        if not self._entity.surroundings:
            return

        self._entity.stop()
        self._entity.perform(Action.DESTROY)

        super().tick()
