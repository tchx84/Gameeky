from .base import Actuator as BaseActuator


class Actuator(BaseActuator):
    name = "portal_switch"

    def tick(self) -> None:
        if self._interactee is None:
            return

        if (target := self._entity.targets()) is None:
            return

        self._interactee.teleport(target.position)

        super().tick()
