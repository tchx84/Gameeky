from .base import Actuator as BaseActuator


class Actuator(BaseActuator):
    name = "damages"
    interactable = False
    activatable = False

    def tick(self) -> None:
        if self._seconds_since_activation() <= self._entity.rate:
            return

        if (surroundings := self._entity.surroundings) is None:
            return

        for entity in surroundings:
            entity.durability -= self._entity.strength

        super().tick()
