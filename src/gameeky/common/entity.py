from typing import Optional, Tuple

from .vector import Vector
from .definitions import Direction, State
from .serializeable import Serializeable


class Entity(Serializeable):
    Signature = Tuple[int, int, Vector.Signature, int, int, bool, float, float]

    def __init__(
        self,
        id: int,
        type_id: int,
        position: Optional[Vector] = None,
        direction: Direction = Direction.EAST,
        state: State = State.IDLING,
        visible: bool = True,
        status: float = 1.0,
        luminance: float = 0.0,
    ) -> None:
        self.id = id
        self.type_id = type_id
        self.direction = direction
        self.state = state
        self.visible = visible
        self.status = status
        self.luminance = luminance

        # Allow to extend on this property in sub-classes
        self._position = position if position else Vector()

    @property
    def position(self) -> Vector:
        return self._position

    @position.setter
    def position(self, position: Vector) -> None:
        self._position = position

    def to_values(self) -> Signature:
        return (
            self.id,
            self.type_id,
            self.position.to_values(),
            self.direction,
            self.state,
            self.visible,
            self.status,
            self.luminance,
        )

    @classmethod
    def from_values(cls, values: Signature) -> "Entity":
        id, type_id, position, direction, state, visible, status, luminance = values
        return cls(
            id,
            type_id,
            Vector.from_values(position),
            Direction(direction),
            State(state),
            visible,
            status,
            luminance,
        )
