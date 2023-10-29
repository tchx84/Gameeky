from typing import Tuple

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
