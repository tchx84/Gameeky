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

from typing import List, Optional

from gi.repository import Gio, GLib, GObject

from .logger import logger


class Monitor(GObject.GObject):
    __gsignals__ = {
        "changed": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    __default__: Optional["Monitor"] = None

    def __init__(self) -> None:
        super().__init__()
        self._cache: List[str] = []
        self._monitors: List[Gio.FileMonitor] = []
        self._timeout_source_id: Optional[int] = None

    def _do_add(self, path: str) -> None:
        if path in self._cache:
            return

        file = Gio.File.new_for_path(path)

        monitor = file.monitor(Gio.FileMonitorFlags.NONE, None)
        monitor.connect("changed", self.__on_changed)

        self._cache.append(path)
        self._monitors.append(monitor)

        logger.debug(f"Monitoring {path}")

    def __on_changed(
        self,
        monitor: Gio.FileMonitor,
        file: Gio.File,
        other: Gio.File,
        event_type: Gio.FileMonitorEvent,
    ) -> None:
        if self._timeout_source_id is not None:
            GLib.Source.remove(self._timeout_source_id)

        self._timeout_source_id = GLib.timeout_add(250, self._notify_change)

    def _notify_change(self, *args) -> int:
        self.emit("changed")
        self._timeout_source_id = None
        return GLib.SOURCE_REMOVE

    def add(self, path: str) -> None:
        GLib.idle_add(self._do_add, path)

    def shutdown(self) -> None:
        if self._timeout_source_id is not None:
            GLib.Source.remove(self._timeout_source_id)

        for monitor in self._monitors:
            monitor.cancel()

        self._cache = []
        self._monitors = []
        self._timeout_source_id = None

        logger.debug("Common.Monitor.shut")

    @classmethod
    def default(cls) -> "Monitor":
        if cls.__default__ is None:
            cls.__default__ = cls()

        return cls.__default__
