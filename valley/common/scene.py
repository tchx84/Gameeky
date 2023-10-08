from typing import List, Optional, Tuple

from .entity import Entity, Vector
from .serializeable import Serializeable


class Scene(Serializeable):
    Signature = Tuple[int, int, Vector.Signature, List[Entity.Signature]]

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

    def to_values(self) -> Signature:
        return (
            self.width,
            self.height,
            self.anchor.to_values(),
            [e.to_values() for e in self.entities],
        )

    @classmethod
    def from_values(cls, values: Signature) -> "Scene":
        width, height, anchor, entities = values
        return cls(
            width,
            height,
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
