from typing import Optional

from gi.repository import GObject

from ...common.scanner import Description
from ...common.entity import Entity as CommonEntity
from ...common.definitions import Direction, State
from ...server.game.entity import EntityRegistry


class Entity(CommonEntity, GObject.GObject):
    __gsignals__ = {
        "changed": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    def __init__(self, *args, **kargs) -> None:
        CommonEntity.__init__(self, *args, **kargs)
        GObject.GObject.__init__(self)
        self._description = Description()

    def reset(self) -> None:
        self.description = self.defaults

    def rotate(self) -> None:
        directions = list(Direction)
        index = directions.index(self.direction)
        direction = directions[(index + 1) % len(directions)]

        self.direction = direction
        self._description.direction = direction.name.lower()
        self.emit("changed")

    @property
    def defaults(self) -> Description:
        return EntityRegistry.find(self.type_id).game.default

    @property
    def description(self) -> Description:
        return self._description

    @description.setter
    def description(self, description: Description) -> None:
        _description = description.__dict__

        for key in _description:
            setattr(self._description, key, _description[key])

        for key in self.__dict__:
            if key not in _description:
                continue

            value = _description[key]

            if key == "state":
                value = State[value.upper()]
            elif key == "direction":
                value = Direction[value.upper()]

            setattr(self, key, value)

        self.emit("changed")

    @property
    def delta(self) -> Optional[Description]:
        description = self.description.__dict__
        defaults = self.defaults.__dict__
        delta = {
            k: description[k] for k in description if description[k] != defaults[k]
        }

        if not delta:
            return None

        return Description(**delta)
