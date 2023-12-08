from .base import Actuator as BaseActuator

from ....common.definitions import Action


class Actuator(BaseActuator):
    name = "propulses"
    interactable = False
    activatable = False

    def tick(self) -> None:
        self._entity.perform(Action.MOVE, self._entity.direction)
