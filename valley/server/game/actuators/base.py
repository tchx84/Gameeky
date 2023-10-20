from __future__ import annotations

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..entity import Entity


class Actuator:
    name = "base"
    interactable = True

    def __init__(self, entity: Entity) -> None:
        self._entity = entity
        self._interactee: Optional[Entity] = None
        self._busy = False

    def prepare(self, interactee: Optional[Entity] = None) -> bool:
        if self._busy is True:
            return False
        if self.interactable is False:
            return False

        self._interactee = interactee
        self._busy = True

        return True

    def tick(self) -> None:
        self._interactee = None
        self._busy = False

    def finished(self) -> bool:
        return self._busy is False
