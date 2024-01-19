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

import os
import importlib.machinery

from typing import Dict, Optional, Type, List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..entity import Entity

from ....common.logger import logger
from ....common.utils import get_time_milliseconds, valid_file


class Actuator:
    name = "base"
    interactable = False
    activatable = False

    def __init__(self, entity: Entity) -> None:
        self._entity = entity
        self._interactee: Optional[Entity] = None
        self._busy = False
        self._activated = False
        self._activated_timestamp = get_time_milliseconds()
        self._initial_activated_timestamp = self._activated_timestamp

    def _seconds_since_activation(self) -> float:
        return (get_time_milliseconds() - self._activated_timestamp) / 1000

    def prepare(self, interactee: Optional[Entity] = None) -> bool:
        if self._busy is True:
            return False
        if self.interactable is False:
            return False

        self._interactee = interactee
        self._busy = True

        return True

    def tick(self) -> None:
        self._interactee = None
        self._busy = False
        self._activated = False
        self._activated_timestamp = get_time_milliseconds()

    def activate(self) -> None:
        self._activated = True

    @property
    def ready(self) -> bool:
        if self._activated_timestamp == self._initial_activated_timestamp:
            return True

        return self._seconds_since_activation() > self._entity.rate or self.activated

    @property
    def entity(self) -> Entity:
        return self._entity

    @property
    def activated(self) -> bool:
        return self.activatable is True and self._activated is True

    @property
    def finished(self) -> bool:
        return self._busy is False


class ActuatorRegistry:
    __actuator_by_name__: Dict[str, Type[Actuator]] = {}

    @classmethod
    def reset(cls) -> None:
        cls.__actuator_by_name__ = {}

    @classmethod
    def register(cls, path: str) -> None:
        if not valid_file(path):
            return

        name = os.path.splitext(os.path.basename(path))[0]

        try:
            loader = importlib.machinery.SourceFileLoader(name, path)
            module = loader.load_module()
            klass = module.Actuator
        except Exception as e:
            logger.error(e)
            return

        if not issubclass(klass, Actuator):
            return

        cls.__actuator_by_name__[name] = module.Actuator

    @classmethod
    def find(cls, name) -> Optional[Type[Actuator]]:
        return cls.__actuator_by_name__.get(name)

    @classmethod
    def names(cls) -> List[str]:
        return list(cls.__actuator_by_name__.keys())
