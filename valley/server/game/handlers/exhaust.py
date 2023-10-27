from .base import Handler as BaseHandler

from ..definitions import Penalty

from ....common.state import State
from ....common.action import Action


class Handler(BaseHandler):
    def prepare(self, value: float) -> bool:
        self._entity.action = Action.EXHAUST

        return super().prepare(value)

    def tick(self) -> None:
        self._entity.state = State.EXHAUSTED

        seconds_since_prepare = self._get_elapsed_seconds_since_prepare()

        if seconds_since_prepare <= self._entity.delay * Penalty.MAX:
            return

        self.finish()

    def finish(self) -> None:
        self._entity.drop(State.IDLING)
        self._entity.perform(Action.IDLE)

        super().finish()
