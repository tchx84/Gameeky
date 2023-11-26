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
    interactable = True
    activatable = True

    def __init__(self, entity: Entity) -> None:
        self._entity = entity
        self._interactee: Optional[Entity] = None
        self._busy = False
        self._activated = False
        self._activated_timestamp = get_time_milliseconds()

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
