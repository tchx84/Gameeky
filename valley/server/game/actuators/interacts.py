from .base import Actuator as BaseActuator

from ....common.action import Action


class Actuator(BaseActuator):
    name = "interacts"
    interactable = False

    def tick(self) -> None:
        if (entity := self._entity.obstacle) is None:
            return

        if entity.interactable is False:
            return

        self._entity.perform(Action.INTERACT)
