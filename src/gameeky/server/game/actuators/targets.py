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

from typing import Optional, TYPE_CHECKING

from .base import Actuator as BaseActuator


if TYPE_CHECKING:
    from ..entity import Entity


class Actuator(BaseActuator):
    name = "targets"
    interactable = False
    activatable = False

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self._target: Optional[Entity] = None

    def tick(self) -> None:
        if self._target is None:
            self._target = self._entity.target
            return

        # If no current target then use this target
        if self._entity.target is None:
            self._entity.target = self._target
            return

        # If current target becomes unavailable then use this target
        if self._entity.target.blocked:
            self._entity.target = self._target
            return

        if self._entity.position != self._target.position:
            return

        # If target is reached then target the next target
        self._target = self._target.target
        self._entity.target = self._target
