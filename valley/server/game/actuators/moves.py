from .base import Actuator as BaseActuator

from ....common.definitions import Action, Direction


class Actuator(BaseActuator):
    name = "moves"
    interactable = False
    activatable = False

    def tick(self) -> None:
        if self._entity.target is None:
            return
        if self._entity.blocked is True:
            return

        delta_x = self._entity.target.position.x - self._entity.position.x
        delta_y = self._entity.target.position.y - self._entity.position.y

        if delta_x == 0 and delta_y == 0:
            return

        if delta_x > 0:
            direction = Direction.EAST
        elif delta_x < 0:
            direction = Direction.WEST
        elif delta_y > 0:
            direction = Direction.SOUTH
        elif delta_y < 0:
            direction = Direction.NORTH

        self._entity.perform(Action.MOVE, direction)
