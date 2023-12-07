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
    def new_from_json(cls, path: str) -> "Description":
        with open(path, "r") as file:
            return json.load(file, object_hook=lambda d: cls(**d))


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
        directory.enumerate_children_async(
            Gio.FILE_ATTRIBUTE_STANDARD_TYPE,
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
            if info.get_file_type() == Gio.FileType.DIRECTORY:
                continue

            path = enumerator.get_child(info).get_path()
            self.emit("found", path)

        self._request_file(enumerator)
