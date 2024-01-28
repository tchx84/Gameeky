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

from .base import Actuator as BaseActuator

if TYPE_CHECKING:
    from ..entity import Entity

from ..definitions import Delay

from ....common.definitions import Action, Direction
from ....common.vector import Vector
from ....common.utils import get_time_milliseconds


class Actuator(BaseActuator):
    name = "follows"
    interactable = False
    activatable = False

    def __init__(self, entity: Entity) -> None:
        super().__init__(entity)
        self._position: Optional[Vector] = None
        self._timestamp: Optional[int] = None

    def _stucked_on_target(self) -> bool:
        if self._position is None:
            self._position = self._entity.position.copy()
        if self._timestamp is None:
            self._timestamp = get_time_milliseconds()

        # Keep track of the last time it actually moved
        if self._position != self._entity.position:
            self._position = self._entity.position.copy()
            self._timestamp = get_time_milliseconds()

        time_on_position = (get_time_milliseconds() - self._timestamp) / 1000

        # If current target becomes unavailable for too long then forget it
        if time_on_position < Delay.MAX:
            return False

        self._entity.target = None
        self._position = None
        self._timestamp = None

        return True

    def tick(self) -> None:
        if self._entity.target is None:
            return
        if self._entity.blocked is True:
            return
        if self._stucked_on_target():
            return

        delta_x = self._entity.target.position.x - self._entity.position.x
        delta_y = self._entity.target.position.y - self._entity.position.y

        if delta_x == 0 and delta_y == 0:
            return

        if delta_x > 0:
            direction = Direction.EAST
        elif delta_x < 0:
            direction = Direction.WEST
        elif delta_y > 0:
            direction = Direction.SOUTH
        elif delta_y < 0:
            direction = Direction.NORTH

        self._entity.perform(Action.MOVE, direction)
