# Copyright (c) 2024 Martín Abente Lahaye.
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


class Dialogue(Serializeable):
    Signature = Tuple[str]

    def __init__(self, text="") -> None:
        self.text = text

    def to_values(self) -> Signature:
        return (self.text,)

    @classmethod
    def from_values(cls, values: Signature) -> "Dialogue":
        return cls(*values)
