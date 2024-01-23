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

from ..definitions import Density


class Actuator(BaseActuator):
    name = "spawns"
    interactable = False
    activatable = True

    def tick(self) -> None:
        if self._entity.rate == 0 and not self.activated:
            return

        if self._seconds_since_activation() < self._entity.rate and not self.activated:
            return

        # Don't spawn entity on top of nothing
        if not (surfaces := self._entity.surfaces):
            return super().tick()

        # Don't spawn entity on top of a solid entity
        for surface in surfaces:
            if surface.density == Density.SOLID:
                return super().tick()

        # Don't spawn entity if already spawned
        for surface in surfaces:
            if surface.type_id == self._entity.target_type:
                return super().tick()

        self._entity.spawn()

        super().tick()
