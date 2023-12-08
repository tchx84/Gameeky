from .base import Actuator as BaseActuator


class Actuator(BaseActuator):
    name = "triggers"
    interactable = False
    activatable = False

    def tick(self) -> None:
        if self._entity.target is None:
            return

        if not self._entity.surroundings:
            return

        if self._seconds_since_activation() <= self._entity.rate:
            return

        self._entity.target.activate()

        super().tick()
