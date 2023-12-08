from __future__ import annotations

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..entity import Entity

from .base import Actuator as BaseActuator


class Actuator(BaseActuator):
    name = "triggers_i"
    interactable = True
    activatable = False

    def prepare(self, interactee: Optional[Entity] = None) -> bool:
        if self._entity.target is None:
            return False

        if self._seconds_since_activation() <= self._entity.rate:
            return False

        return super().prepare(interactee)

    def tick(self) -> None:
        if self._interactee is None:
            return

        if self._entity.target is None:
            return

        self._entity.target.activate()

        super().tick()
