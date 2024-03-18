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

import json

from typing import Any, Optional
from types import SimpleNamespace

from gi.repository import Gio, GLib, GObject


class DescriptionEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Description):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


class Description(SimpleNamespace):
    def to_json(self) -> str:
        return json.dumps(self, cls=DescriptionEncoder, sort_keys=True, indent=4)

    @classmethod
    def new_from_json(cls, path: str, **kargs) -> "Description":
        with open(path, "r") as file:
            return json.load(file, object_hook=lambda d: cls(**(d | kargs)))


class Scanner(GObject.GObject):
    __gsignals__ = {
        "found": (GObject.SignalFlags.RUN_LAST, None, (str,)),
        "done": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    def __init__(self, path: str) -> None:
        super().__init__()
        self._path = path

    def scan(self) -> None:
        directory = Gio.File.new_for_path(self._path)

        if not directory.query_exists():
            self.emit("done")
            return

        directory.enumerate_children_async(
            f"{Gio.FILE_ATTRIBUTE_STANDARD_TYPE},{Gio.FILE_ATTRIBUTE_STANDARD_NAME}",
            Gio.FileQueryInfoFlags.NONE,
            GLib.PRIORITY_DEFAULT,
            None,
            self.__on_enumerate_children,
            None,
        )

    def _request_file(self, enumerator: Gio.FileEnumerator) -> None:
        enumerator.next_files_async(
            1,
            GLib.PRIORITY_DEFAULT,
            None,
            self.__on_next_files,
            enumerator,
        )

    def __on_enumerate_children(
        self,
        source: GObject.GObject,
        result: Gio.AsyncResult,
        data: Optional[Any] = None,
    ) -> None:
        self._request_file(source.enumerate_children_finish(result))

    def __on_next_files(
        self,
        source: GObject.GObject,
        result: Gio.AsyncResult,
        enumerator: Gio.FileEnumerator,
    ) -> None:
        infos = source.next_files_finish(result)

        if not infos:
            self.emit("done")
            return

        for info in infos:
            path = enumerator.get_child(info).get_path()
            self.emit("found", path)

        self._request_file(enumerator)
