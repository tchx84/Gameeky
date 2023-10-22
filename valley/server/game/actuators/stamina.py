from .base import Actuator as BaseActuator

from ..definitions import Cost

from ....common.action import Action
from ....common.utils import get_time_milliseconds


class Actuator(BaseActuator):
    __stamina_cost_by_action__ = {
        Action.MOVE: Cost.MAX,
        Action.USE: Cost.MAX * 4,
        Action.TAKE: Cost.MAX * 4,
    }

    name = "stamina"
    interactable = False

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self._timestamp_tick = get_time_milliseconds()

    def tick(self) -> None:
        timestamp = get_time_milliseconds()
        seconds_since_tick = (timestamp - self._timestamp_tick) / 1000

        cost = self.__stamina_cost_by_action__.get(self._entity.action, Cost.MIN)
        gain = abs(cost) * self._entity.recovery
        self._entity.stamina += (gain - (cost - Cost.MIN)) * seconds_since_tick

        if self._entity.stamina <= 0:
            self._entity.perform(Action.EXHAUST)

        self._timestamp_tick = timestamp
