from .base import Handler as BaseHandler

from ..definitions import Density, Delay

from ....common.definitions import State
from ....common.action import Action


class Handler(BaseHandler):
    def prepare(self, value: float) -> bool:
        self._entity.action = Action.DESTROY
        self._entity.density = Density.VOID
        self._entity.position.z -= 1

        return super().prepare(value)

    def tick(self) -> None:
        self._entity.state = State.DESTROYING

        if self._get_elapsed_seconds_since_prepare() <= Delay.MAX:
            return

        self.finish()

    def finish(self) -> None:
        self._entity.state = State.DESTROYED
        self._entity.drop()
        self._entity.fall()

        super().finish()

    def cancel(self) -> None:
        pass
