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

from typing import Dict, Tuple, List, Optional

from ...common.utils import clamp
from ...common.vector import Vector
from ...common.entity import Entity
from ...common.definitions import Direction


class SpatialPartition:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self._entity_by_position: Dict[Tuple[int, int], List[Entity]] = {}

    def add(self, entity: Entity, z: Optional[int] = None) -> None:
        position = (
            math.floor(entity.position.x),
            math.floor(entity.position.y),
        )

        if position not in self._entity_by_position:
            self._entity_by_position[position] = []

        # Depth should only be modified here
        entity.position.z = (
            z if z is not None else len(self._entity_by_position[position])
        )

        self._entity_by_position[position].append(entity)

    def remove(self, entity: Entity) -> None:
        position = (
            math.floor(entity.position.x),
            math.floor(entity.position.y),
        )

        self._entity_by_position[position].remove(entity)

        if len(self._entity_by_position[position]) == 0:
            del self._entity_by_position[position]

    def get_position_for_direction(
        self, position: Vector, direction: Direction
    ) -> Vector:
        position = position.copy()

        if direction == Direction.EAST:
            position.x += 1
        if direction == Direction.SOUTH:
            position.y += 1
        if direction == Direction.WEST:
            position.x -= 1
        if direction == Direction.NORTH:
            position.y -= 1

        # Don't go outside'of the scene
        position.x = clamp(self.width - 1, 0, position.x)
        position.y = clamp(self.height - 1, 0, position.y)

        return position

    def find_by_position(self, position: Vector) -> List[Entity]:
        x = math.floor(position.x)
        y = math.floor(position.y)

        return self._entity_by_position.get((x, y), [])

    def find_by_direction(self, entity: Entity) -> List[Entity]:
        x = entity.position.x
        y = entity.position.y

        # XXX Everything should probably account for direction
        x = math.ceil(x) if entity.direction == Direction.EAST else math.floor(x)
        y = math.ceil(y) if entity.direction == Direction.SOUTH else math.floor(y)

        if entity.direction == Direction.EAST:
            x += 1
        elif entity.direction == Direction.NORTH:
            y -= 1
        elif entity.direction == Direction.WEST:
            x -= 1
        elif entity.direction == Direction.SOUTH:
            y += 1

        return self._entity_by_position.get((x, y), [])

    def find_by_distance(
        self,
        target: Entity,
        distance_x: int,
        distance_y: int,
    ) -> List[Entity]:
        entities = []

        from_range_x = math.floor(max(target.position.x - distance_x, 0))
        to_range_x = math.floor(min(target.position.x + distance_x + 1, self.width))

        from_range_y = math.floor(max(target.position.y - distance_y, 0))
        to_range_y = math.floor(min(target.position.y + distance_y + 1, self.height))

        for y in range(from_range_y, to_range_y):
            for x in range(from_range_x, to_range_x):
                entities += self._entity_by_position.get((x, y), [])

        return entities
