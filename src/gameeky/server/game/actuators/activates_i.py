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

from __future__ import annotations

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..entity import Entity

from .base import Actuator as BaseActuator

from ..definitions import Density


class Actuator(BaseActuator):
    name = "activates_i"
    interactable = True
    activatable = False

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self._target: Optional[Entity] = None

    def prepare(self, interactee: Optional[Entity] = None) -> bool:
        if self._seconds_since_activation() <= self._entity.rate:
            return False

        if (entity := self._entity.overlay) is None:
            return False

        if entity.density != Density.SOLID:
            return False

        if not self._entity.targets(entity):
            return False

        self._target = entity

        return super().prepare(interactee)

    def tick(self) -> None:
        if self._interactee is None:
            return

        if self._target is None:
            return

        self._target.activate()

        super().tick()
