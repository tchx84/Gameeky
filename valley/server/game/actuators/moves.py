from .base import Actuator as BaseActuator

from ....common.direction import Direction
from ....common.action import Action


class Actuator(BaseActuator):
    name = "moves"
    interactable = False

    def tick(self) -> None:
        if self._entity.target is None:
            return
        if self._entity.blocked is True:
            return

        delta_x = self._entity.target.position.x - self._entity.position.x
        delta_y = self._entity.target.position.y - self._entity.position.y

        if delta_x == 0 and delta_y == 0:
            self._entity.target = self._entity.target.target
            return

        if delta_x > 0:
            direction = Direction.RIGHT
        elif delta_x < 0:
            direction = Direction.LEFT
        elif delta_y > 0:
            direction = Direction.DOWN
        elif delta_y < 0:
            direction = Direction.UP

        self._entity.perform(Action.MOVE, direction)
