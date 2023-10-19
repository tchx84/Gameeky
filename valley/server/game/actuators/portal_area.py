from .base import Actuator as BaseActuator

from ..definitions import Density


class Actuator(BaseActuator):
    name = "portal_area"

    def tick(self) -> None:
        entities = self._partition.find_by_distance(
            target=self._entity,
            distance_x=self._entity.radius,  # type: ignore
            distance_y=self._entity.radius,  # type: ignore
        )

        interactees = []
        for entity in entities:
            if entity.density == Density.SOLID:  # type: ignore
                interactees.append(entity)

        if not interactees:
            return

        target = self._entity.targets()  # type: ignore
        if target is None:
            return

        for interactee in interactees:
            interactee.teleport(target.position)  # type: ignore
