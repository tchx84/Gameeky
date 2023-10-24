from enum import IntEnum

from typing import Optional, Tuple

from .state import State
from .direction import Direction
from .serializeable import Serializeable


class Vector(Serializeable):
    Signature = Tuple[float, float, float]

    def __init__(self, x: float = 0, y: float = 0, z: float = 0) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector):
            return NotImplemented

        return self.x == other.x and self.y == other.y and self.z == other.z

    def to_values(self) -> Signature:
        return (self.x, self.y, self.z)

    def copy(self) -> "Vector":
        return self.__class__(*self.to_values())

    @classmethod
    def from_values(cls, values: Signature) -> "Vector":
        return cls(*values)


class EntityType(IntEnum):
    EMPTY = 0


class Entity(Serializeable):
    Signature = Tuple[int, int, Vector.Signature, int, int, bool]

    def __init__(
        self,
        id: int,
        type_id: int,
        position: Optional[Vector] = None,
        direction: Direction = Direction.RIGHT,
        state: State = State.IDLING,
        visible: bool = True,
    ) -> None:
        self.id = id
        self.type_id = type_id
        self.direction = direction
        self.state = state
        self.visible = visible

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
        )

    @classmethod
    def from_values(cls, values: Signature) -> "Entity":
        id, type_id, position, direction, state, visible = values
        return cls(
            id,
            type_id,
            Vector.from_values(position),
            Direction(direction),
            State(state),
            visible,
        )
