from __future__ import annotations

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..entity import Entity

from ....common.utils import get_time_milliseconds


class Actuator:
    name = "base"
    interactable = True
    activatable = True

    def __init__(self, entity: Entity) -> None:
        self._entity = entity
        self._interactee: Optional[Entity] = None
        self._busy = False
        self._activated = False
        self._activated_timestamp = get_time_milliseconds()

    def _seconds_since_activation(self) -> float:
        return (get_time_milliseconds() - self._activated_timestamp) / 1000

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
        self._activated = False
        self._activated_timestamp = get_time_milliseconds()

    def activate(self) -> None:
        self._activated = True

    @property
    def activated(self) -> bool:
        return self.activatable is True and self._activated is True

    def finished(self) -> bool:
        return self._busy is False
