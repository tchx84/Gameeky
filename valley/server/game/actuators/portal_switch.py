from .base import Actuator as BaseActuator


class Actuator(BaseActuator):
    name = "portal_switch"
    interactable = True

    def tick(self) -> None:
        if self._interactee is None:
            return

        if (target := self._entity.target) is None:
            return

        self._interactee.position = target.position
        self._interactee.destination = target.position_at(self._interactee.direction)

        super().tick()
