import random

from .base import Actuator as BaseActuator

from ....common.definitions import Action, Direction


class Actuator(BaseActuator):
    name = "roams"
    interactable = False
    activatable = False

    def tick(self) -> None:
        self._entity.perform(Action.MOVE, random.choice(list(Direction)))
