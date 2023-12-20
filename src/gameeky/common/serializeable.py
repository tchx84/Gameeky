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

import json

from typing import Any


class Serializeable(object):
    Signature = Any

    def to_values(self) -> Any:
        raise NotImplementedError

    @classmethod
    def from_values(cls, values: Any) -> Any:
        raise NotImplementedError

    def serialize(self) -> bytes:
        return json.dumps(self.to_values()).encode("UTF-8")

    @classmethod
    def deserialize(cls, data: bytes) -> Any:
        values = json.loads(data.decode("UTF-8"))
        return cls.from_values(values)
