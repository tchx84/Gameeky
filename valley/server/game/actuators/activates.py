from .base import Actuator as BaseActuator

from ..definitions import Density


class Actuator(BaseActuator):
    name = "activates"
    interactable = False
    activatable = False

    def tick(self) -> None:
        if self._seconds_since_activation() <= self._entity.rate:
            return

        if (target := self._entity.overlay) is None:
            return

        if target.density != Density.SOLID:
            return

        target.activate()

        super().tick()
