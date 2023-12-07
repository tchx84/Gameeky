from .base import Actuator as BaseActuator

from ....common.definitions import State


class Actuator(BaseActuator):
    name = "transmutes"
    interactable = False
    activatable = True

    def tick(self) -> None:
        if self._seconds_since_activation() < self._entity.rate and not self.activated:
            return

        self._entity.state = State.DESTROYED
        self._entity.spawn()

        super().tick()
