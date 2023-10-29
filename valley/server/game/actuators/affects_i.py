from .base import Actuator as BaseActuator


class Actuator(BaseActuator):
    name = "affects_i"
    interactable = True
    activatable = False

    def tick(self) -> None:
        if self._interactee is None:
            return

        self._interactee.stamina += self._entity.stamina
        self._interactee.durability += self._entity.durability
        self._interactee.durability -= self._entity.strength

        super().tick()
