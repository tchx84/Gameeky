from .base import Handler as BaseHandler

from ..definitions import Density

from ....common.state import State
from ....common.action import Action
from ....common.entity import EntityType


class Handler(BaseHandler):
    def prepare(self, value: float) -> bool:
        if self._entity.held is None:
            return False

        if self._get_elapsed_seconds_since_finish() < self._entity.delay:
            return False

        self._entity.action = Action.USE

        return super().prepare(value)

    def tick(self) -> None:
        if self._entity.held is None:
            return

        self._entity.state = State.USING

        if self._get_elapsed_seconds_since_tick() <= self._entity.delay:
            return

        if self._entity.held.spawns != EntityType.EMPTY:
            self._entity.spawn()

        seconds_since_prepare = self._get_elapsed_seconds_since_prepare()

        for target in self._entity.obstacles:
            if target.visible is False:
                continue
            if target.density != Density.SOLID:
                continue
            if target is self._entity.held:
                continue

            # Wear the target
            target.durability -= self._entity.held.strength * seconds_since_prepare

            # Restore the target
            target.durability += self._entity.held.durability * seconds_since_prepare
            target.stamina += self._entity.held.stamina * seconds_since_prepare

        self.finish()

    def finished(self) -> None:
        self._entity.action = Action.IDLE
        self._entity.state = State.IDLING

        super().finish()
