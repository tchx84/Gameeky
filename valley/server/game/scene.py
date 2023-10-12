import math

from typing import Dict, Tuple, List

from gi.repository import GLib, GObject

from .entity import Entity, EntityRegistry

from ...common.action import Action
from ...common.entity import EntityType, Vector
from ...common.entity import Entity as CommonEntity
from ...common.scanner import Description
from ...common.direction import Direction
from ...common.definitions import TICK, TILES_X, TILES_Y
from ...common.scene import Scene as CommonScene


class Space:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self._entity_by_position: Dict[Tuple[int, int], List[CommonEntity]] = {}

    def add(self, entity: CommonEntity) -> None:
        position = (
            math.floor(entity.position.x),
            math.floor(entity.position.y),
        )

        if position not in self._entity_by_position:
            self._entity_by_position[position] = []

        self._entity_by_position[position].append(entity)

    def remove(self, entity: CommonEntity) -> None:
        position = (
            math.floor(entity.position.x),
            math.floor(entity.position.y),
        )

        self._entity_by_position[position].remove(entity)

        if len(self._entity_by_position[position]) == 0:
            del self._entity_by_position[position]

    def find_by_direction(
        self,
        this_entity: CommonEntity,
        direction: Direction,
    ) -> List[CommonEntity]:
        x = round(this_entity.position.x)
        y = round(this_entity.position.y)

        if direction == Direction.RIGHT:
            x += 1
        elif direction == Direction.UP:
            y -= 1
        elif direction == Direction.LEFT:
            x -= 1
        elif direction == Direction.DOWN:
            y += 1

        return self._entity_by_position.get((x, y), [])

    def find_by_distance(
        self,
        target: CommonEntity,
        distance_x: int,
        distance_y: int,
    ) -> List[CommonEntity]:
        entities: List[CommonEntity] = []

        from_range_x = math.floor(max(target.position.x - distance_x, 0))
        to_range_x = math.floor(min(target.position.x + distance_x, self.width))

        from_range_y = math.floor(max(target.position.y - distance_y, 0))
        to_range_y = math.floor(min(target.position.y + distance_y, self.height))

        for y in range(from_range_y, to_range_y):
            for x in range(from_range_x, to_range_x):
                for entity in self._entity_by_position.get((x, y), []):
                    entities.append(entity)

        return entities


class Scene(CommonScene, GObject.GObject):
    def __init__(self, width: int, height: int, spawnpoint: Vector) -> None:
        CommonScene.__init__(self, width, height)
        GObject.GObject.__init__(self)

        self._index = 0
        self._entity_by_id: Dict[int, Entity] = {}
        self._space = Space(width=width, height=height)

        self.spawnpoint = spawnpoint

        GLib.timeout_add(TICK, self.__on_scene_ticked)

    def __on_scene_ticked(self) -> int:
        self.tick()
        return GLib.SOURCE_CONTINUE

    def tick(self):
        for entity in self._entity_by_id.values():
            self._space.remove(entity)

            if entity.action == Action.IDLE:
                entity.idle()
            if entity.action == Action.MOVE:
                obstacles = self._space.find_by_direction(entity, entity.direction)
                entity.move(obstacles)

            self._space.add(entity)

    def add(self, type_id: int, position: Vector) -> int:
        entity = EntityRegistry.new_from_values(
            id=self._index,
            type_id=type_id,
            position=position,
        )

        self._index += 1
        self._entity_by_id[entity.id] = entity
        self._space.add(entity)

        self.entities.append(entity)

        return entity.id

    def update(self, entity_id: int, action: Action, value: float) -> None:
        entity = self._entity_by_id[entity_id]

        if action == Action.IDLE:
            pass
        if action == Action.MOVE:
            entity.direction = Direction(int(value))

        entity.action = action

    def remove(self, entity_id: int) -> None:
        entity = self._entity_by_id[entity_id]

        del self._entity_by_id[entity_id]
        self._space.remove(entity)
        self.entities.remove(entity)

    def prepare_for_entity_id(self, entity_id: int) -> CommonScene:
        entity = self._entity_by_id[entity_id]
        distance_x = math.ceil(TILES_X / 2)
        distance_y = math.ceil(TILES_Y / 2)

        entities = self._space.find_by_distance(
            target=entity,
            distance_x=distance_x,
            distance_y=distance_y,
        )

        return CommonScene(
            width=TILES_X,
            height=TILES_Y,
            anchor=entity.position,
            entities=entities,
        )

    @classmethod
    def new_from_description(cls, description: Description) -> "Scene":
        scene = cls(
            width=description.width,
            height=description.height,
            spawnpoint=Vector(
                x=description.spawnpoint.x,
                y=description.spawnpoint.y,
                z=description.spawnpoint.z,
            ),
        )

        for depth, layer in enumerate(description.layers):
            for index, type_id in enumerate(layer.entities):
                if type_id == EntityType.EMPTY:
                    continue

                position = Vector()
                position.x = index % scene.width
                position.y = int(index / scene.width)
                position.z = depth

                scene.add(type_id, position)

        return scene
