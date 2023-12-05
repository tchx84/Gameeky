from .base import Actuator as BaseActuator


class Actuator(BaseActuator):
    name = "aggroes"
    interactable = False
    activatable = False

    def tick(self) -> None:
        target = None

        for entity in self._entity.surroundings:
            if entity.type_id == self._entity.type_id:
                continue
            if entity.type_id == self._entity.target_type:
                target = entity
                break
            if entity.removable or entity.playable:
                target = entity
                break

        self._entity.target = target
