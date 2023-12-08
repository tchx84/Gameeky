from typing import List, Optional, Tuple

from .vector import Vector
from .entity import Entity
from .serializeable import Serializeable


class Scene(Serializeable):
    Signature = Tuple[int, int, float, Vector.Signature, List[Entity.Signature]]

    def __init__(
        self,
        width: int,
        height: int,
        time: float = 0.0,
        anchor: Optional[Vector] = None,
        entities: Optional[List[Entity]] = None,
    ) -> None:
        self.width = width
        self.height = height
        self.time = time
        self.anchor = anchor if anchor is not None else Vector()
        self.entities = entities if entities is not None else []

    def to_values(self) -> Signature:
        return (
            self.width,
            self.height,
            self.time,
            self.anchor.to_values(),
            [e.to_values() for e in self.entities],
        )

    @classmethod
    def from_values(cls, values: Signature) -> "Scene":
        width, height, time, anchor, entities = values
        return cls(
            width,
            height,
            time,
            Vector.from_values(anchor),
            [Entity.from_values(e) for e in entities],
        )


class SceneRequest(Serializeable):
    Signature = Tuple[int]

    def __init__(self, session_id: int) -> None:
        self.session_id = session_id

    def to_values(self) -> Signature:
        return (self.session_id,)

    @classmethod
    def from_values(cls, values: Signature) -> "SceneRequest":
        return cls(*values)
