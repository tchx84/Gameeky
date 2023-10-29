from .base import Actuator as BaseActuator

from ....common.definitions import Action


class Actuator(BaseActuator):
    name = "destroys_i"
    interactable = True
    activatable = True

    def tick(self) -> None:
        if self._interactee is None and self.activated is False:
            return

        self._entity.stop()
        self._entity.perform(Action.DESTROY)

        super().tick()
