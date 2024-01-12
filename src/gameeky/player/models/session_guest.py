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

from typing import Optional
from gi.repository import GObject, Gtk

from ...client.game.service import Service
from ...client.game.scene import Scene as SceneModel
from ...client.game.stats import Stats as StatsModel
from ...client.input.keyboard import Keyboard
from ...client.input.cursor import Cursor
from ...client.graphics.entity import EntityRegistry as EntityGraphicsRegistry
from ...client.sound.entity import EntityRegistry as EntitySoundRegistry
from ...client.sound.scene import Scene as SceneSound

from ...common.logger import logger
from ...common.utils import get_project_path, set_project_path
from ...common.scanner import Scanner, Description
from ...common.definitions import TILES_X, TILES_Y
from ...common.threaded import Threaded


class SessionGuest(Threaded):
    __gsignals__ = {
        "initializing": (GObject.SignalFlags.RUN_LAST, None, ()),
        "started": (GObject.SignalFlags.RUN_LAST, None, ()),
        "failed": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    def __init__(
        self,
        project_path: str,
        address: str,
        session_port: int,
        messages_port: int,
        widget: Gtk.Widget,
    ) -> None:
        super().__init__()

        self._project_path = project_path
        self._address = address
        self._session_port = session_port
        self._messages_port = messages_port

        self._widget = widget

        self._service: Optional[Service] = None
        self._scene_model: Optional[SceneModel] = None
        self._stats_model: Optional[StatsModel] = None
        self._keyboard: Optional[Keyboard] = None
        self._cursor: Optional[Cursor] = None
        self._sound: Optional[SceneSound] = None

    def _setup(self) -> None:
        self._service = Service(
            address=self._address,
            session_port=self._session_port,
            messages_port=self._messages_port,
            context=self._context,
        )

        self._scene_model = SceneModel(
            width=TILES_X,
            height=TILES_Y,
            service=self._service,
        )

        self._stats_model = StatsModel(
            service=self._service,
        )

        self._keyboard = Keyboard(
            widget=self._widget,
            service=self._service,
            context=self._context,
        )

        self._cursor = Cursor(
            widget=self._widget,
            model=self._scene_model,
            service=self._service,
        )

        self._sound = SceneSound()
        self._sound.model = self._scene_model

        self._service.connect("registered", self.__on_registered)
        self._service.connect("failed", self.__on_registered_failed)
        self._service.register()

    def _scan(self) -> None:
        EntityGraphicsRegistry.reset()
        EntitySoundRegistry.reset()

        self._scanner = Scanner(path=get_project_path("entities"))
        self._scanner.connect("found", self.__on_scanner_found)
        self._scanner.connect("done", self.__on_scanner_done)
        self._scanner.scan()

    def __on_scanner_found(self, scanner: Scanner, path: str) -> None:
        description = Description.new_from_json(path)
        EntityGraphicsRegistry.register(description)
        EntitySoundRegistry.register(description)

    def __on_scanner_done(self, scanner: Scanner) -> None:
        try:
            self._setup()
        except Exception as e:
            logger.error(e)
            self.emit("failed")

    def __on_registered(self, *args) -> None:
        self.emit("started")

    def __on_registered_failed(self, *args) -> None:
        self.emit("failed")

    def do_run(self) -> None:
        set_project_path(self._project_path)

        try:
            self._scan()
        except Exception as e:
            logger.error(e)
            self.emit("failed")
        else:
            self.emit("initializing")

    def do_shutdown(self, *args) -> None:
        if self._scene_model is not None:
            self._scene_model.shutdown()
        if self._stats_model is not None:
            self._stats_model.shutdown()
        if self._keyboard is not None:
            self._keyboard.shutdown()
        if self._cursor is not None:
            self._cursor.shutdown()
        if self._sound is not None:
            self._sound.shutdown()
        if self._service is not None:
            self._service.unregister()

        logger.debug("Client.Session.shut")

    @property
    def scene(self) -> Optional[SceneModel]:
        return self._scene_model

    @property
    def stats(self) -> Optional[StatsModel]:
        return self._stats_model
