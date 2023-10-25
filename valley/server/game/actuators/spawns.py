from .base import Actuator as BaseActuator


class Actuator(BaseActuator):
    name = "spawns"
    interactable = False
    activatable = True

    def tick(self) -> None:
        if self._seconds_since_activation() > self._entity.rate or self.activated:
            self._entity.spawn()

        super().tick()
