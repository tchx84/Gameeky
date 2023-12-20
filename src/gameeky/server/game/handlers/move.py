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

import math

from .base import Handler as BaseHandler

from ..definitions import Density

from ....common.utils import division
from ....common.definitions import Action, Direction, State


class Handler(BaseHandler):
    def prepare(self, value: float) -> bool:
        self._entity.direction = Direction(int(value))

        obstacles = self._entity.obstacles

        # Don't allow walking in empty space
        if not obstacles:
            return False

        for obstacle in obstacles:
            if obstacle.density == Density.SOLID:
                return False

        self._entity.action = Action.MOVE
        self._entity.destination = obstacles[-1].position

        return super().prepare(value)

    def tick(self) -> None:
        if (surface := self._entity.surface) is None:
            return

        self._entity.state = State.MOVING

        ratio = division(self._entity.strength, self._entity.weight)
        friction = Density.SOLID - surface.density
        seconds_since_tick = self._get_elapsed_seconds_since_tick()

        distance = ratio * friction * seconds_since_tick

        delta_x = self._entity.destination.x - self._entity.position.x
        delta_y = self._entity.destination.y - self._entity.position.y

        distance_x = min(distance, abs(delta_x))
        distance_y = min(distance, abs(delta_y))

        direction_x = math.copysign(1, delta_x)
        direction_y = math.copysign(1, delta_y)

        position = self._entity.position.copy()
        position.x += distance_x * direction_x
        position.y += distance_y * direction_y

        self._entity.position = position

        super().tick()

        if self._entity.position.x != self._entity.destination.x:
            return
        if self._entity.position.y != self._entity.destination.y:
            return

        self.finish()

    def finish(self):
        self._entity.secure()
        self._entity.action = Action.IDLE
        self._entity.state = State.IDLING

        super().finish()
