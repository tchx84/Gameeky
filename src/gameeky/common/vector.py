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

        return self.x == other.x and self.y == other.y

    def to_values(self) -> Signature:
        return (self.x, self.y, self.z)

    def copy(self) -> "Vector":
        return self.__class__(self.x, self.y, self.z)

    @classmethod
    def from_values(cls, values: Signature) -> "Vector":
        return cls(*values)
