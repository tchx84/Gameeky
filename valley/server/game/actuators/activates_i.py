from __future__ import annotations

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..entity import Entity

from .base import Actuator as BaseActuator

from ..definitions import Density


class Actuator(BaseActuator):
    name = "activates_i"
    interactable = True
    activatable = False

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self._target: Optional[Entity] = None

    def prepare(self, interactee: Optional[Entity] = None) -> bool:
        if self._seconds_since_activation() <= self._entity.rate:
            return False

        if (entity := self._entity.overlay) is None:
            return False

        if entity.density != Density.SOLID:
            return False

        self._target = entity

        return super().prepare(interactee)

    def tick(self) -> None:
        if self._interactee is None:
            return

        if self._target is None:
            return

        self._target.activate()

        super().tick()
