from typing import Optional

from gi.repository import GObject

from ...common.utils import get_data_path
from ...common.scanner import Scanner, Description

from ...client.graphics.entity import EntityRegistry as EntityGraphicsRegistry
from ...server.game.entity import EntityRegistry as EntityGameRegistry


class Entity(GObject.GObject):
    __gsignals__ = {
        "started": (GObject.SignalFlags.RUN_LAST, None, ()),
        "registered": (GObject.SignalFlags.RUN_LAST, None, (object,)),
        "finished": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    def __init__(self) -> None:
        super().__init__()
        self._scanner: Optional[Scanner] = None

    def scan(self) -> None:
        EntityGraphicsRegistry.reset()
        EntityGameRegistry.reset()

        self._scanner = Scanner(path=get_data_path("entities"))
        self._scanner.connect("found", self.__on_scanner_found)
        self._scanner.connect("done", self.__on_scanner_done)
        self._scanner.scan()

        self.emit("started")

    def __on_scanner_found(self, scanner: Scanner, description: Description) -> None:
        EntityGraphicsRegistry.register(description)
        EntityGameRegistry.register(description)
        self.emit("registered", description)

    def __on_scanner_done(self, scanner: Scanner) -> None:
        self.emit("finished")
