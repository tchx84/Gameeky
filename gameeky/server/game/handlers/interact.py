from typing import List

from .base import Handler as BaseHandler

from ..actuators.base import Actuator

from ....common.logger import logger
from ....common.definitions import Action, State


class Handler(BaseHandler):
    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self._actuating: List[Actuator] = []

    def prepare(self, value: float) -> bool:
        actuating = []

        for entity in self._entity.obstacles:
            for actuator in entity.actuators:
                try:
                    if actuator.prepare(interactee=self._entity) is True:
                        actuating.append(actuator)
                except Exception as e:
                    logger.error(e)

        if not actuating:
            return False

        self._entity.action = Action.INTERACT
        self._actuating = actuating

        return super().prepare(value)

    def tick(self) -> None:
        self._entity.state = State.INTERACTING

        for actuator in self._actuating:
            if actuator.finished is False:
                return

        self.finish()

    def finish(self) -> None:
        self._entity.perform(Action.IDLE)
        self._actuating = []

        super().finish()
