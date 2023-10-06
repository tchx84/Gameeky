from typing import List, Optional, Tuple

from .entity import Entity, Vector
from .serializeable import Serializeable


class Scene(Serializeable):
    def __init__(
        self,
        width: int,
        height: int,
        anchor: Optional[Vector] = None,
        entities: Optional[List[Entity]] = None,
    ) -> None:
        self.width = width
        self.height = height
        self.anchor = anchor if anchor is not None else Vector()
        self.entities = entities if entities is not None else []

    def to_values(self):
        return (
            self.width,
            self.height,
            self.anchor.to_values(),
            [e.to_values() for e in self.entities],
        )

    @classmethod
    def from_values(
        cls,
        values: Tuple[
            int,
            int,
            Tuple[float, float],
            List[Tuple[int, Tuple[float, ...], float, float, int]],
        ],
    ) -> "Scene":
        width, height, anchor, entities = values
        return cls(
            width,
            height,
            Vector.from_values(anchor),
            [Entity.from_values(e) for e in entities],
        )


class SceneRequest(Serializeable):
    def __init__(self, session_id: int) -> None:
        self.session_id = session_id

    def to_values(self):
        return (self.session_id,)

    @classmethod
    def from_values(cls, values: Tuple[int]) -> "SceneRequest":
        return cls(*values)
