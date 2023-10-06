from typing import List, Optional, Tuple

from gi.repository import GLib

from .entity import Entity
from .serializeable import Serializeable


class Scene(Serializeable):
    SIGNATURE = "(iiav)"

    def __init__(
        self, width: int, height: int, entities: Optional[List[Entity]] = None
    ) -> None:
        self.width = width
        self.height = height
        self.entities = entities if entities is not None else []

    def to_variant(self) -> GLib.Variant:
        return GLib.Variant(
            self.SIGNATURE,
            (self.width, self.height, [e.to_variant() for e in self.entities]),
        )

    @classmethod
    def from_values(
        cls,
        values: Tuple[int, int, List[Tuple[int, Tuple[float, ...], float, float, int]]],
    ) -> "Scene":
        width, height, entities = values
        return cls(width, height, [Entity.from_values(e) for e in entities])


class SceneRequest(Serializeable):
    SIGNATURE = "(i)"

    def __init__(self, session_id: int) -> None:
        self.session_id = session_id

    def to_variant(self) -> GLib.Variant:
        return GLib.Variant(self.SIGNATURE, (self.session_id,))

    @classmethod
    def from_values(cls, values: Tuple[int]) -> "SceneRequest":
        return cls(*values)
