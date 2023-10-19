from .base import Actuator as BaseActuator


class Actuator(BaseActuator):
    name = "portal"

    def tick(self) -> None:
        if self._interactee is None:
            return

        if (target := self._entity.targets()) is None:  # type: ignore
            return

        self._interactee.teleport(target.position)  # type: ignore

        super().tick()
