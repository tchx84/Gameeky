from __future__ import annotations

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..entity import Entity

from .base import Actuator as BaseActuator

from ....common.definitions import Action


class Actuator(BaseActuator):
    name = "destroys_i"
    interactable = True
    activatable = True

    def prepare(self, interactee: Optional[Entity] = None) -> bool:
        if interactee is None:
            return False

        if not self._entity.targets(interactee):
            return False

        return super().prepare(interactee)

    def tick(self) -> None:
        if self._interactee is None and self.activated is False:
            return

        self._entity.stop()
        self._entity.perform(Action.DESTROY)

        super().tick()
