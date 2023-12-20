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


class Stats(Serializeable):
    Signature = Tuple[float, float, int]

    def __init__(
        self, durability: float = 0, stamina: float = 0, held: int = 0
    ) -> None:
        self.durability = durability
        self.stamina = stamina
        self.held = held

    def to_values(self) -> Signature:
        return (self.durability, self.stamina, self.held)

    @classmethod
    def from_values(cls, values: Signature) -> "Stats":
        return cls(*values)


class StatsRequest(Serializeable):
    Signature = Tuple[int]

    def __init__(self, session_id: int) -> None:
        self.session_id = session_id

    def to_values(self) -> Signature:
        return (self.session_id,)

    @classmethod
    def from_values(cls, values: Signature) -> "StatsRequest":
        return cls(*values)
