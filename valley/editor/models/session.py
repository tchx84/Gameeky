from gi.repository import GObject

from ...common.utils import get_data_path
from ...common.scanner import Scanner, Description
from ...common.monitor import Monitor

from ...client.graphics.entity import EntityRegistry as EntityGraphicsRegistry
from ...server.game.entity import EntityRegistry as EntityGameRegistry
from ...server.game.actuators.base import ActuatorRegistry


class Session(GObject.GObject):
    __gsignals__ = {
        "started": (GObject.SignalFlags.RUN_LAST, None, ()),
        "registered": (GObject.SignalFlags.RUN_LAST, None, (object,)),
        "ready": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    def __init__(self) -> None:
        super().__init__()
        Monitor.default().shutdown()

    def scan(self) -> None:
        EntityGraphicsRegistry.reset()
        EntityGameRegistry.reset()

        scanner = Scanner(path=get_data_path("entities"))
        scanner.connect("found", self.__on_entities_scanner_found)
        scanner.connect("done", self.__on_entities_scanner_done)
        scanner.scan()

        self.emit("started")

    def __on_entities_scanner_found(self, scanner: Scanner, path: str) -> None:
        description = Description.new_from_json(path)

        Monitor.default().add(path)
        EntityGraphicsRegistry.register(description)
        EntityGameRegistry.register(description)

        self.emit("registered", description)

    def __on_entities_scanner_done(self, scanner: Scanner) -> None:
        ActuatorRegistry.reset()

        scanner = Scanner(path=get_data_path("actuators"))
        scanner.connect("found", self.__on_actuators_scanner_found)
        scanner.connect("done", self.__on_actuators_scanner_done)
        scanner.scan()

    def __on_actuators_scanner_found(self, scanner: Scanner, path: str) -> None:
        Monitor.default().add(path)
        ActuatorRegistry.register(path)

    def __on_actuators_scanner_done(self, scanner: Scanner) -> None:
        self.emit("ready")
