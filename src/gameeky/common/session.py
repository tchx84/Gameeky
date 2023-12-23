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

from typing import Tuple, Optional

from .serializeable import Serializeable


class Session(Serializeable):
    Signature = Tuple[int, Optional[int]]

    def __init__(self, id: int, error: Optional[int]) -> None:
        self.id = id
        self.error = error

    def to_values(self) -> Signature:
        return (self.id, self.error)

    @classmethod
    def from_values(cls, values: Signature) -> "Session":
        return cls(*values)


class SessionRequest(Serializeable):
    Signature = Tuple[int, str]

    def __init__(self, type_id: int, version: str) -> None:
        self.type_id = type_id
        self.version = version

    def to_values(self) -> Signature:
        return (self.type_id, self.version)

    @classmethod
    def from_values(cls, values: Signature) -> "SessionRequest":
        return cls(*values)
