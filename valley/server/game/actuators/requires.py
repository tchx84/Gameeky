from .base import Actuator as BaseActuator


class Actuator(BaseActuator):
    name = "requires"
    interactable = False
    activatable = False

    def tick(self) -> None:
        if self._entity.target is None:
            return

        if self._seconds_since_activation() <= self._entity.rate:
            return

        if (requirement := self._entity.overlay) is None:
            return

        if requirement.visible is False:
            return

        if requirement.type_id != self._entity.spawns:
            return

        self._entity.target.activate()

        super().tick()
