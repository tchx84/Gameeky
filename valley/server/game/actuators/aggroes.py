from .base import Actuator as BaseActuator


class Actuator(BaseActuator):
    name = "aggroes"
    interactable = False
    activatable = False

    def tick(self) -> None:
        target = None

        for entity in self._entity.surroundings:
            if entity is self._entity:
                continue
            if entity.mutable:
                target = entity
                break

        if target is None:
            return

        self._entity.target = target
