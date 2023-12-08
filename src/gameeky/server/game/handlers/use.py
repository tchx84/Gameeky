from .base import Handler as BaseHandler

from ..definitions import Density, Delay

from ....common.definitions import Action, EntityType, State


class Handler(BaseHandler):
    def prepare(self, value: float) -> bool:
        if self._entity.held is None:
            return False

        if self._entity.held.usable is False:
            return False

        if self._get_elapsed_seconds_since_finish() < self._entity.delay:
            return False

        self._entity.action = Action.USE

        return super().prepare(value)

    def tick(self) -> None:
        if self._entity.held is None:
            return

        self._entity.state = State.USING

        if self._get_elapsed_seconds_since_prepare() <= Delay.MAX:
            return

        if self._entity.held.target_type != EntityType.EMPTY:
            self._entity.spawn()

        for target in self._entity.obstacles:
            if target.visible is False:
                continue
            if target.density != Density.SOLID:
                continue
            if target is self._entity.held:
                continue

            # Wear the target
            target.durability -= self._entity.held.strength

            # Restore the target
            target.durability += self._entity.held.durability
            target.stamina += self._entity.held.stamina

        self.finish()

    def finished(self) -> None:
        self._entity.action = Action.IDLE
        self._entity.state = State.IDLING

        super().finish()
