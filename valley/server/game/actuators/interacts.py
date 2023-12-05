from .base import Actuator as BaseActuator

from ....common.definitions import Action


class Actuator(BaseActuator):
    name = "interacts"
    interactable = False
    activatable = False

    def tick(self) -> None:
        if (entity := self._entity.obstacle) is None:
            return

        if entity.interactable is False:
            return

        if not self._entity.targets(entity):
            return

        self._entity.perform(Action.INTERACT)
