from gi.repository import GObject

from ...common.utils import get_data_path
from ...common.scanner import Scanner
from ...common.monitor import Monitor

from ...server.game.actuators.base import ActuatorRegistry


class Session(GObject.GObject):
    __gsignals__ = {
        "started": (GObject.SignalFlags.RUN_LAST, None, ()),
        "ready": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    def __init__(self) -> None:
        super().__init__()
        Monitor.default().shutdown()
        Monitor.default().add(get_data_path("actuators"))

    def scan(self) -> None:
        ActuatorRegistry.reset()

        scanner = Scanner(path=get_data_path("actuators"))
        scanner.connect("found", self.__on_scanner_found)
        scanner.connect("done", self.__on_scanner_done)
        scanner.scan()

        self.emit("started")

    def __on_scanner_found(self, scanner: Scanner, path: str) -> None:
        ActuatorRegistry.register(path)

    def __on_scanner_done(self, scanner: Scanner) -> None:
        self.emit("ready")
