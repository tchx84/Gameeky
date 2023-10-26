from .base import Actuator as BaseActuator

from ..definitions import Recovery


class Actuator(BaseActuator):
    name = "deteriorates"
    interactable = False
    activatable = False

    def tick(self) -> None:
        self._entity.durability -= (
            Recovery.MAX - self._entity.recovery
        ) * self._seconds_since_activation()

        super().tick()
