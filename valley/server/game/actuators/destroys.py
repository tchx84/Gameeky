from .base import Actuator as BaseActuator

from ....common.action import Action


class Actuator(BaseActuator):
    name = "destroys"
    interactable = False

    def tick(self) -> None:
        if self._entity.durability <= 0:
            self._entity.perform(Action.DESTROY)
