import math

from gi.repository import GObject

from ...common.entity import Entity as CommonEntity
from ...common.scene import Scene as CommonScene
from ...common.scanner import Description
from ...common.vector import Vector
from ...common.definitions import EntityType, Direction, State

from ...server.game.entity import EntityRegistry


class Scene(CommonScene, GObject.GObject):
    __gsignals__ = {
        "ticked": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    def __init__(self) -> None:
        CommonScene.__init__(self, 0, 0)
        GObject.GObject.__init__(self)
        self._index = 0

    def add(self, type_id: int, x: int, y: int, z: int) -> None:
        default = EntityRegistry.find(type_id).game.default

        entity = CommonEntity(
            id=self._index,
            type_id=type_id,
            position=Vector(x, y, z),
            visible=default.visible,
            luminance=default.luminance,
            direction=Direction[default.direction.upper()],
            state=State[default.state.upper()],
        )

        self.entities.append(entity)
        self._index += 1

        self.emit("ticked")

    @property
    def ratio(self) -> float:
        return self.width / self.height

    @property
    def description(self) -> Description:
        return Description()

    @description.setter
    def description(self, description: Description) -> None:
        self.time = 0.0
        self.width = description.width
        self.height = description.height

        # XXX figure out where the 0.5 offset is coming from
        self.anchor = Vector(
            x=math.floor(self.width / 2) - 0.5,
            y=math.floor(self.height / 2),
        )

        for depth, layer in enumerate(description.layers):
            for index, type_id in enumerate(layer.entities):
                if type_id == EntityType.EMPTY:
                    continue

                x = index % self.width
                y = int(index / self.width)
                z = depth

                self.add(type_id, x, y, z)
