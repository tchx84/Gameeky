from .base import Handler as BaseHandler

from ....common.definitions import State
from ....common.action import Action


class Handler(BaseHandler):
    def prepare(self, value: float) -> bool:
        if self._entity.held is None:
            return False

        self._entity.action = Action.DROP

        return super().prepare(value)

    def tick(self) -> None:
        if self._entity.held is None:
            return

        self._entity.state = State.DROPPING

        seconds_since_prepare = self._get_elapsed_seconds_since_prepare()
        ratio = self._entity.held.weight / self._entity.strength
        super().tick()

        if seconds_since_prepare <= self._entity.delay * ratio:
            return

        self.finish()

    def finish(self) -> None:
        self._entity.drop(State.IDLING)
        self._entity.action = Action.IDLE
        self._entity.state = State.IDLING

        super().finish()
