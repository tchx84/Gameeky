from typing import List, Optional

from .entity import Entity
from .serializeable import Serializeable


class Scene(Serializeable):
    def __init__(self, entities: Optional[List[Entity]] = None) -> None:
        self.entities = entities if entities is not None else []
