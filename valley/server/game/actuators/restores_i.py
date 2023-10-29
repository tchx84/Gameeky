from .base import Actuator as BaseActuator

from ....common.definitions import Action


class Actuator(BaseActuator):
    name = "restores_i"
    interactable = True
    activatable = False

    def tick(self) -> None:
        if self._interactee is None:
            return

        self._interactee.stamina += self._entity.stamina
        self._interactee.durability += self._entity.durability

        self._entity.perform(Action.DESTROY)

        super().tick()
