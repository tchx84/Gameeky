from typing import Optional, TYPE_CHECKING

from .base import Actuator as BaseActuator


if TYPE_CHECKING:
    from ..entity import Entity


class Actuator(BaseActuator):
    name = "targets"
    interactable = False

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self._original_target: Optional[Entity] = None

    def tick(self) -> None:
        if self._original_target is None:
            self._original_target = self._entity.target

        if self._entity.target is None:
            self._entity.target = self._original_target
            return

        if self._entity.target.blocked:
            self._entity.target = self._original_target
            return

        if self._entity.position == self._entity.target.position:
            if self._entity.target.visible is False:
                self._entity.target = self._entity.target.target
                return

        target: Optional[Entity] = None

        for entity in self._entity.surroundings:
            if entity.name:
                target = entity

        if target is None:
            return

        self._entity.target = target
