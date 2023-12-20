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

from .definitions import Action
from .serializeable import Serializeable


class Message(Serializeable):
    Signature = Tuple[int, int, float, int]

    def __init__(
        self,
        session_id: int,
        action: Action = Action.IDLE,
        value: float = 0,
        sequence: int = 0,
    ) -> None:
        self.session_id = session_id
        self.action = action
        self.value = value
        self.sequence = sequence

    def to_values(self) -> Signature:
        return (self.session_id, self.action, self.value, self.sequence)

    @classmethod
    def from_values(cls, values: Signature) -> "Message":
        session_id, action, value, sequence = values
        return cls(session_id, Action(action), value, sequence)
