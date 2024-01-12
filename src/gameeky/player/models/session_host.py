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

from typing import Optional, Callable
from gi.repository import GObject

from ...common.logger import logger
from ...common.utils import get_project_path, set_project_path
from ...common.scanner import Scanner, Description
from ...common.threaded import Threaded
from ...common.monitor import Monitor

from ...server.game.service import Service
from ...server.game.entity import EntityRegistry as EntityGameRegistry
from ...server.game.actuators.base import ActuatorRegistry


class SessionHost(Threaded):
    __gsignals__ = {
        "initializing": (GObject.SignalFlags.RUN_LAST, None, ()),
        "started": (GObject.SignalFlags.RUN_LAST, None, ()),
        "failed": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    def __init__(
        self,
        project_path: str,
        scene: str,
        clients: int,
        session_port: int,
        messages_port: int,
    ) -> None:
        super().__init__()

        self._project_path = project_path
        self._scene = scene
        self._clients = clients
        self._session_port = session_port
        self._messages_port = messages_port

        self._service: Optional[Service] = None

    def _setup(self) -> None:
        Monitor.default().add(get_project_path("actuators"))
        Monitor.default().add(get_project_path("entities"))
        Monitor.default().add(get_project_path(self._scene))

        self._service = Service(
            scene=self._scene,
            clients=self._clients,
            session_port=self._session_port,
            messages_port=self._messages_port,
            context=self.context,
        )

    def _scan_entities(self) -> None:
        EntityGameRegistry.reset()

        scanner = Scanner(path=get_project_path("entities"))
        scanner.connect("found", self.__on_entities_scanner_found)
        scanner.connect("done", self.__on_entities_scanner_done)
        scanner.scan()

    def __on_entities_scanner_found(self, scanner: Scanner, path: str) -> None:
        EntityGameRegistry.register(Description.new_from_json(path))

    def __on_entities_scanner_done(self, scanner: Scanner) -> None:
        ActuatorRegistry.reset()

        scanner = Scanner(path=get_project_path("actuators"))
        scanner.connect("found", self.__on_actuators_scanner_found)
        scanner.connect("done", self.__on_actuators_scanner_done)
        scanner.scan()

    def __on_actuators_scanner_found(self, scanner: Scanner, path: str) -> None:
        ActuatorRegistry.register(path)

    def __on_actuators_scanner_done(self, scanner: Scanner) -> None:
        try:
            self._setup()
        except Exception as e:
            logger.error(e)
            self.emit("failed")
        else:
            self.emit("started")

    def do_run(self) -> None:
        set_project_path(self._project_path)

        try:
            self._scan_entities()
        except Exception as e:
            logger.error(e)
            self.emit("failed")
        else:
            self.emit("initializing")

    def do_shutdown(self, *args) -> None:
        if self._service is not None:
            self._service.shutdown()

        logger.debug("Server.Session.shut")

    def do_request_description(self, callback: Callable, path: str) -> None:
        if self._service is None:
            return

        callback(path, self._service.scene.description)

    def request_description(self, callback: Callable, path: str) -> None:
        self.exec(self.do_request_description, (callback, path))

    @property
    def scene_name(self) -> Optional[str]:
        if self._service is None:
            return None

        return self._service.scene.name
