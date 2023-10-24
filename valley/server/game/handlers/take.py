from .base import Handler as BaseHandler

from ..definitions import Density

from ....common.state import State
from ....common.action import Action


class Handler(BaseHandler):
    def prepare(self, value: float) -> bool:
        if self._entity.held is not None:
            return False

        entity = self._entity.obstacle

        if entity is None:
            return False
        if entity.density != Density.SOLID:
            return False
        if entity.visible is False:
            return False
        if entity.state == State.MOVING:
            return False

        self._entity.held = entity
        self._entity.held.density = Density.VOID
        self._entity.held.state = State.HELD
        self._entity.held.visible = not self._entity.held.equippable

        self._entity.action = Action.TAKE

        return super().prepare(value)

    def tick(self) -> None:
        if self._entity.held is None:
            return

        self._entity.state = State.TAKING

        seconds_since_prepare = self._get_elapsed_seconds_since_prepare()
        ratio = self._entity.held.weight / self._entity.strength

        if seconds_since_prepare <= self._entity.delay * ratio:
            return

        self.finish()

    def finish(self) -> None:
        self._entity.action = Action.IDLE
        self._entity.state = State.IDLING

        super().finish()
