from .base import Actuator as BaseActuator

from ..definitions import Density

from ....common.definitions import Action


class Actuator(BaseActuator):
    name = "uses"
    interactable = False
    activatable = False

    def tick(self) -> None:
        if (entity := self._entity.obstacle) is None:
            return

        if entity.density != Density.SOLID:
            return

        if not entity.name:
            return

        self._entity.perform(Action.USE)
