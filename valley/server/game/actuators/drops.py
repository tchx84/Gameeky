from .base import Actuator as BaseActuator


class Actuator(BaseActuator):
    name = "drops"
    interactable = False
    activatable = False

    def tick(self) -> None:
        if self._entity.busy is True:
            return

        if self._entity.durability > 0:
            return

        self._entity.spawn()
