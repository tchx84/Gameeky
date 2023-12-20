# Copyright (c) 2023 Martín Abente Lahaye.
#
# This file is part of Gameeky
# (see gameeky.tchx84.dev).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

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
