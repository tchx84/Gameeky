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

from .base import Handler as BaseHandler

from ..definitions import Density

from ....common.definitions import Action, State


class Handler(BaseHandler):
    def prepare(self, value: float) -> bool:
        if self._entity.held is not None:
            return False

        entity = self._entity.obstacle

        if entity is None:
            return False
        if entity.takeable is False:
            return False
        if entity.visible is False:
            return False

        self._entity.held = entity
        self._entity.held.stop()
        self._entity.held.density = Density.VOID
        self._entity.held.state = State.HELD
        self._entity.held.visible = not self._entity.held.usable

        self._entity.action = Action.TAKE

        return super().prepare(value)

    def tick(self) -> None:
        if self._entity.held is None:
            return

        self._entity.state = State.TAKING

        seconds_since_prepare = self._get_elapsed_seconds_since_prepare()
        ratio = self._entity.held.weight / self._entity.strength

        if seconds_since_prepare <= self._entity.delay * ratio:
            return

        self.finish()

    def finish(self) -> None:
        self._entity.action = Action.IDLE
        self._entity.state = State.IDLING

        super().finish()
