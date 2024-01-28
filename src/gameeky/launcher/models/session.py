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

import os

from gi.repository import GObject

from ...common.logger import logger
from ...common.monitor import Monitor
from ...common.scanner import Scanner, Description
from ...common.utils import get_projects_path, valid_project


class Session(GObject.GObject):
    __gsignals__ = {
        "found": (GObject.SignalFlags.RUN_LAST, None, (str, object)),
    }

    def __init__(self) -> None:
        super().__init__()
        Monitor.default().shutdown()
        Monitor.default().add(get_projects_path())

    def scan(self) -> None:
        scanner = Scanner(path=get_projects_path())
        scanner.connect("found", self.__on_scanner_found)
        scanner.scan()

    def __on_scanner_found(self, scanner: Scanner, path: str) -> None:
        if not valid_project(path):
            return

        summary_path = os.path.join(path, "gameeky.project")
        description = Description.new_from_json(summary_path)

        self.emit("found", path, description)
        logger.debug(f"Found {summary_path}")

    def shutdown(self) -> None:
        Monitor.default().shutdown()
