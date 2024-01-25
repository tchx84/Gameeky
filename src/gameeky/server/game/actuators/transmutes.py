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

from .base import Actuator as BaseActuator

from ....common.definitions import State


class Actuator(BaseActuator):
    name = "transmutes"
    interactable = False
    activatable = True

    def tick(self) -> None:
        # Don't keep spawning entities if already reached final state
        if self._entity.blocked:
            return

        if not self.ready:
            return

        self._entity.state = State.DESTROYED
        self._entity.spawn()

        super().tick()
