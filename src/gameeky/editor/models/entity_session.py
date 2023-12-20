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

from gi.repository import GObject

from ...common.utils import get_project_path
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
        Monitor.default().add(get_project_path("actuators"))

    def scan(self) -> None:
        ActuatorRegistry.reset()

        scanner = Scanner(path=get_project_path("actuators"))
        scanner.connect("found", self.__on_scanner_found)
        scanner.connect("done", self.__on_scanner_done)
        scanner.scan()

        self.emit("started")

    def __on_scanner_found(self, scanner: Scanner, path: str) -> None:
        ActuatorRegistry.register(path)

    def __on_scanner_done(self, scanner: Scanner) -> None:
        self.emit("ready")
