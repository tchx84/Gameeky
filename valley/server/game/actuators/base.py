from typing import Optional

from ....common.entity import Entity


class Actuator:
    name = "base"

    def __init__(self, entity: Entity) -> None:
        self._entity = entity
        self._interactee: Optional[Entity] = None
        self._busy = False

    def prepare(self, interactee: Optional[Entity] = None) -> None:
        self._interactee = interactee
        self._busy = True

    def tick(self) -> None:
        self._interactee = None
        self._busy = False

    def finished(self) -> bool:
        return self._busy is False
