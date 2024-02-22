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

from .base import Handler as BaseHandler

from ....common.definitions import Action, State, Direction


class Handler(BaseHandler):
    def prepare(self, value: float) -> bool:
        self._entity.action = Action.ROTATE
        self._entity.direction = Direction(int(value))

        return super().prepare(value)

    def tick(self) -> None:
        self._entity.state = State.IDLING

        self.finish()
