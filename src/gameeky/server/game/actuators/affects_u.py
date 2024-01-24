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

from .base import Actuator as BaseActuator


class Actuator(BaseActuator):
    name = "affects_u"
    interactable = False
    activatable = True

    def tick(self) -> None:
        if not self.activated:
            return super().tick()

        if (surroundings := self._entity.surroundings) is None:
            return super().tick()

        for entity in surroundings:
            if not self._entity.targets(entity):
                continue

            entity.stamina += self._entity.stamina
            entity.durability += self._entity.durability
            entity.durability -= self._entity.strength

        return super().tick()
