from .base import Actuator as BaseActuator


class Actuator(BaseActuator):
    name = "damages"
    interactable = False
    activatable = False

    def tick(self) -> None:
        if (surroundings := self._entity.surroundings) is None:
            return

        seconds = self._seconds_since_activation()

        for entity in surroundings:
            entity.durability -= self._entity.strength * seconds

        super().tick()
