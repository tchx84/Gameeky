from .base import Actuator as BaseActuator


class Actuator(BaseActuator):
    name = "portal_area"

    def tick(self) -> None:
        if (target := self._entity.targets()) is None:
            return

        for interactee in self._entity.surroundings():
            interactee.teleport(target.position)
