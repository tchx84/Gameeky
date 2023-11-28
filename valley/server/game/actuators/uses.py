from .base import Actuator as BaseActuator

from ..definitions import Density

from ....common.definitions import Action


class Actuator(BaseActuator):
    name = "uses"
    interactable = False
    activatable = False

    def tick(self) -> None:
        if self._entity.held is None:
            return

        if (entity := self._entity.obstacle) is None:
            return

        if entity.type_id == self._entity.type_id:
            return

        if entity.density != Density.SOLID:
            return

        if not entity.removable and not entity.playable:
            return

        self._entity.perform(Action.USE)
