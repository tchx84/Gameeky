from .base import Actuator as BaseActuator


class Actuator(BaseActuator):
    name = "portal_area"
    interactable = False

    def tick(self) -> None:
        if (target := self._entity.target) is None:
            return

        for interactee in self._entity.surroundings:
            interactee.position = target.position
            interactee.destination = target.position_at(interactee.direction)
