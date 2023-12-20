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

from gi.repository import GLib, GObject

from ..common.logger import logger
from ..common.utils import wait, get_time_milliseconds
from ..common.entity import Entity
from ..common.scene import Scene
from ..common.stats import Stats
from ..common.session import Session
from ..common.definitions import (
    Action,
    Direction,
    TICK,
    DEFAULT_ADDRESS,
    DEFAULT_SESSION_PORT,
    DEFAULT_MESSAGES_PORT,
    DEFAULT_SCENE_PORT,
    DEFAULT_STATS_PORT,
)

from ..client.game.service import Service


class Game(GObject.GObject):
    __gsignals__ = {
        "updated": (GObject.SignalFlags.RUN_LAST, None, (int,)),
    }

    def __init__(
        self,
        address: str = DEFAULT_ADDRESS,
        session_port: int = DEFAULT_SESSION_PORT,
        messages_port: int = DEFAULT_MESSAGES_PORT,
        scene_port: int = DEFAULT_SCENE_PORT,
        stats_port: int = DEFAULT_STATS_PORT,
    ) -> None:
        super().__init__()
        self._address = address
        self._session_port = session_port
        self._messages_port = messages_port
        self._scene_port = scene_port
        self._stats_port = stats_port

        self._entity: Optional[Entity] = None
        self._scene: Optional[Scene] = None
        self._stats: Optional[Stats] = None

        self._session: Optional[Session] = None
        self._service: Optional[Service] = None

        self._timestamp = get_time_milliseconds()
        self._mainloop: Optional[GLib.MainLoop] = None

    def _update(self) -> int:
        if self._service is None:
            return GLib.SOURCE_CONTINUE

        self._service.request_stats()
        self._service.request_scene()

        return GLib.SOURCE_CONTINUE

    def __on_registered(self, service: Service, session: Session) -> None:
        if self._service is None:
            return

        self._session = session
        self._service.connect("stats-updated", self.__on_stats_updated)
        self._service.connect("scene-updated", self.__on_scene_updated)

        GLib.timeout_add(TICK, self._update)

    def __on_stats_updated(self, service: Service, stats: Stats) -> None:
        self._stats = stats

    def __on_scene_updated(self, service: Service, scene: Scene) -> None:
        self._scene = scene
        self._entity = next((e for e in scene.entities if e.position == scene.anchor))

        self.emit("updated", get_time_milliseconds() - self._timestamp)

    def run(self) -> None:
        logger.debug("run")

        GLib.idle_add(self.join)

        self._mainloop = GLib.MainLoop()
        self._mainloop.run()

    def quit(self) -> None:
        logger.debug("quit")

        if self._service is not None:
            self._service.unregister()
        if self._mainloop is not None:
            self._mainloop.quit()

    def join(self) -> None:
        logger.debug("join")

        self._service = Service(
            self._address,
            self._session_port,
            self._messages_port,
            self._scene_port,
            self._stats_port,
            GLib.MainContext.default(),
        )
        self._service.connect("registered", self.__on_registered)
        self._service.register()

        wait(int(TICK))

    def perform(self, action: Action, value: float = 0, time: int = 0) -> None:
        if self._service is None:
            return

        logger.debug(Action(action).name.lower())
        self._service.message(action, value)

        wait(time)

    def idle(self, time: int = 0) -> None:
        self.perform(Action.IDLE, time=time)

    def move(self, direction: Direction, time: int = 0) -> None:
        self.perform(Action.MOVE, direction, time)

    def take(self, time: int = 0) -> None:
        self.perform(Action.TAKE, time=time)

    def drop(self, time: int = 0) -> None:
        self.perform(Action.DROP, time=time)

    def use(self, time: int = 0) -> None:
        self.perform(Action.USE, time=time)

    def interact(self, time: int = 0) -> None:
        self.perform(Action.INTERACT, time=time)

    @property
    def entity(self) -> Optional[Entity]:
        return self._entity

    @property
    def scene(self) -> Optional[Scene]:
        return self._scene

    @property
    def stats(self) -> Optional[Stats]:
        return self._stats
