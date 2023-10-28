from .base import Actuator as BaseActuator

from ....common.action import Action


class Actuator(BaseActuator):
    name = "propulses"
    interactable = False
    activatable = False

    def tick(self) -> None:
        self._entity.perform(Action.MOVE, self._entity.direction)
