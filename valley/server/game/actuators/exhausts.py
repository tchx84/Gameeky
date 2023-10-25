from .base import Actuator as BaseActuator

from ..definitions import Cost

from ....common.action import Action


class Actuator(BaseActuator):
    __stamina_cost_by_action__ = {
        Action.MOVE: Cost.MAX,
        Action.USE: Cost.MAX * 4,
        Action.TAKE: Cost.MAX * 4,
    }

    name = "exhausts"
    interactable = False
    activatable = True

    def tick(self) -> None:
        seconds = self._seconds_since_activation()

        cost = self.__stamina_cost_by_action__.get(self._entity.action, Cost.MIN)
        gain = abs(cost) * self._entity.recovery
        self._entity.stamina += (gain - (cost - Cost.MIN)) * seconds

        if self._entity.stamina <= 0 or self.activated is True:
            self._entity.perform(Action.EXHAUST)

        super().tick()
