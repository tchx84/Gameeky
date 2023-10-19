from .base import Actuator as BaseActuator


class Actuator(BaseActuator):
    name = "portal"

    def tick(self) -> None:
        if self._interactee is None:
            return

        target = self._entity.targets()  # type: ignore
        if target is None:
            return

        self._interactee.teleport(target.position)  # type: ignore

        self._interactee = None
        self._busy = False

        super().tick()
