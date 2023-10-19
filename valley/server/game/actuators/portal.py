from .base import Actuator as BaseActuator


class Actuator(BaseActuator):
    name = "portal"

    def tick(self) -> None:
        if self._interactee is None:
            return

        target = self._entity.targets()  # type: ignore
        if target is None:
            return

        self._partition.remove(self._interactee)

        self._interactee.position.x = target.position.x
        self._interactee.position.y = target.position.y
        self._interactee.position.z = target.position.z

        self._partition.add(self._interactee)

        self._interactee = None
        self._busy = False

        super().tick()
