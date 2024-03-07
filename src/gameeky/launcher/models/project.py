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
import shutil
import zipfile

from typing import List, Tuple, Optional

from gi.repository import GObject, GLib

from ...common.logger import logger
from ...common.scanner import Description
from ...common.utils import get_projects_path, find_new_name


class Project:
    @classmethod
    def write(cls, path: str, description: Description) -> None:
        with open(os.path.join(path, "gameeky.project"), "w") as file:
            file.write(description.to_json())

    @classmethod
    def sanitize(cls, name: str) -> str:
        return os.path.basename(os.path.abspath(name)).strip()

    @classmethod
    def create(cls, description: Description) -> str:
        project_path = os.path.join(get_projects_path(), cls.sanitize(description.name))

        os.makedirs(os.path.join(project_path, "actuators"))
        os.makedirs(os.path.join(project_path, "assets"))
        os.makedirs(os.path.join(project_path, "entities"))
        os.makedirs(os.path.join(project_path, "scenes"))

        cls.write(project_path, description)

        return project_path

    @classmethod
    def rename(cls, path: str, description: Description) -> str:
        projects_path = os.path.dirname(path)
        project_path = os.path.join(projects_path, cls.sanitize(description.name))

        os.rename(path, project_path)
        cls.write(project_path, description)

        return project_path

    @classmethod
    def copy(cls, path: str, description: Description) -> str:
        description.name = find_new_name(get_projects_path(), description.name)
        project_path = os.path.join(get_projects_path(), cls.sanitize(description.name))

        os.mkdir(project_path)

        for directory in ["actuators", "assets", "entities", "scenes"]:
            shutil.copytree(
                os.path.join(path, directory),
                os.path.join(project_path, directory),
            )

        cls.write(project_path, description)

        return project_path

    @classmethod
    def remove(cls, path: str) -> None:
        shutil.rmtree(path)


class Exporter(GObject.GObject):
    __gsignals__ = {
        "started": (GObject.SignalFlags.RUN_LAST, None, ()),
        "progressed": (GObject.SignalFlags.RUN_LAST, None, (float,)),
        "finished": (GObject.SignalFlags.RUN_LAST, None, ()),
        "failed": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    def __init__(self, source: str, target: str) -> None:
        super().__init__()
        self._total = 0
        self._items: List[Tuple[str, str]] = []
        self._source = source
        self._target = target
        self._zip: Optional[zipfile.ZipFile] = None

    def start(self) -> None:
        self._collect("gameeky.project")
        self._collect("actuators")
        self._collect("assets")
        self._collect("entities")
        self._collect("scenes")

        try:
            self._zip = zipfile.ZipFile(
                self._target,
                "w",
                zipfile.ZIP_DEFLATED,
                strict_timestamps=False,
            )
        except Exception as e:
            logger.error(e)
            self.emit("failed")
        else:
            self._total = len(self._items)
            self.emit("started")
            GLib.idle_add(self._do_step)

    def _collect(self, name: str) -> None:
        source = os.path.join(self._source, name)

        self._items.append((source, name))

        if os.path.isfile(source):
            return

        for root, dirs, files in os.walk(source):
            for file in files:
                self._items.append(
                    (
                        os.path.join(root, file),
                        os.path.relpath(
                            os.path.join(root, file),
                            os.path.join(source, ".."),
                        ),
                    )
                )

    def _do_step(self) -> None:
        if self._zip is None:
            return

        if not self._items:
            self._finish()
            return

        try:
            self._zip.write(*self._items.pop())
        except Exception as e:
            logger.error(e)
            self.emit("failed")
        else:
            self.emit("progressed", 1.0 - len(self._items) / self._total)
            GLib.idle_add(self._do_step)

    def _finish(self) -> None:
        if self._zip is not None:
            self._zip.close()

        self.emit("finished")


class Importer(GObject.GObject):
    __gsignals__ = {
        "started": (GObject.SignalFlags.RUN_LAST, None, ()),
        "progressed": (GObject.SignalFlags.RUN_LAST, None, (float,)),
        "finished": (GObject.SignalFlags.RUN_LAST, None, ()),
        "failed": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    def __init__(self, source: str, target: str) -> None:
        super().__init__()
        self._total = 0
        self._items: List[str] = []
        self._source = source
        self._target = target
        self._zip: Optional[zipfile.ZipFile] = None

    def start(self) -> None:
        try:
            self._zip = zipfile.ZipFile(
                self._source,
                "r",
                zipfile.ZIP_DEFLATED,
                strict_timestamps=False,
            )
        except Exception as e:
            logger.error(e)
            self.emit("failed")
        else:
            self._collect(self._zip.namelist())
            self.emit("started")
            GLib.idle_add(self._do_step)

    def _do_step(self) -> None:
        if self._zip is None:
            return

        if not self._items:
            self._finish()
            return

        try:
            self._zip.extract(self._items.pop(), self._target)
        except Exception as e:
            logger.error(e)
            self.emit("failed")
        else:
            self.emit("progressed", 1.0 - len(self._items) / self._total)
            GLib.idle_add(self._do_step)

    def _collect(self, names: List[str]) -> None:
        for name in names:
            if not os.path.isabs(name):
                self._items.append(name)

        self._total = len(self._items)

    def _finish(self) -> None:
        if self._zip is not None:
            self._zip.close()

        self.emit("finished")
