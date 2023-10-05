from typing import List, Optional, Tuple

from gi.repository import GLib

from .entity import Entity
from .serializeable import Serializeable


class Scene(Serializeable):
    SIGNATURE = "av"

    def __init__(self, entities: Optional[List[Entity]] = None) -> None:
        self.entities = entities if entities is not None else []

    def to_variant(self) -> GLib.Variant:
        return GLib.Variant(self.SIGNATURE, [e.to_variant() for e in self.entities])

    @classmethod
    def from_values(
        cls,
        values: List[Tuple[int, Tuple[float, ...], float, float, int]],
    ) -> "Scene":
        return cls([Entity.from_values(e) for e in values])
