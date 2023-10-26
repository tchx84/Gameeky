from .base import Actuator as BaseActuator


class Actuator(BaseActuator):
    name = "spawns"
    interactable = False
    activatable = True

    def tick(self) -> None:
        if self._seconds_since_activation() < self._entity.rate and not self.activated:
            return

        self._entity.spawn()

        super().tick()
