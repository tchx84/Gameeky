from typing import Optional
from gi.repository import GObject, GLib

from ...common.logger import logger
from ...common.utils import get_data_path, set_data_path
from ...common.scanner import Scanner, Description

from ...server.game.service import Service
from ...server.game.entity import EntityRegistry as EntityGameRegistry


class SessionHost(GObject.GObject):
    __gsignals__ = {
        "initializing": (GObject.SignalFlags.RUN_LAST, None, ()),
        "started": (GObject.SignalFlags.RUN_LAST, None, ()),
        "failed": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    def __init__(
        self,
        data_path: str,
        scene: str,
        clients: int,
        session_port: int,
        messages_port: int,
        scene_port: int,
        stats_port: int,
    ) -> None:
        super().__init__()

        self._data_path = data_path
        self._scene = scene
        self._clients = clients
        self._session_port = session_port
        self._messages_port = messages_port
        self._scene_port = scene_port
        self._stats_port = stats_port

        self._service: Optional[Service] = None

    def _setup(self) -> None:
        self._service = Service(
            scene=self._scene,
            clients=self._clients,
            session_port=self._session_port,
            messages_port=self._messages_port,
            scene_port=self._scene_port,
            stats_port=self._stats_port,
            context=GLib.MainContext.default(),
        )

    def _scan(self) -> None:
        EntityGameRegistry.reset()

        self._scanner = Scanner(path=get_data_path("entities"))
        self._scanner.connect("found", self.__on_scanner_found)
        self._scanner.connect("done", self.__on_scanner_done)
        self._scanner.scan()

    def __on_scanner_found(self, scanner: Scanner, description: Description) -> None:
        EntityGameRegistry.register(description)

    def __on_scanner_done(self, scanner: Scanner) -> None:
        try:
            self._setup()
        except Exception as e:
            logger.error(e)
            self.emit("failed")
        else:
            self.emit("started")

    def create(self) -> None:
        set_data_path(self._data_path)

        try:
            self._scan()
        except Exception as e:
            logger.error(e)
            self.emit("failed")
        else:
            self.emit("initializing")

    def shutdown(self) -> None:
        if self._service is not None:
            self._service.shutdown()

        logger.info("Server.Session.shut")
