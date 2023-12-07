from __future__ import annotations

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..entity import Entity

from .base import Actuator as BaseActuator


class Actuator(BaseActuator):
    name = "affects_i"
    interactable = True
    activatable = False

    def prepare(self, interactee: Optional[Entity] = None) -> bool:
        if interactee is None:
            return False

        if not self._entity.targets(interactee):
            return False

        return super().prepare(interactee)

    def tick(self) -> None:
        if self._interactee is None:
            return

        self._interactee.stamina += self._entity.stamina
        self._interactee.durability += self._entity.durability
        self._interactee.durability -= self._entity.strength

        super().tick()
