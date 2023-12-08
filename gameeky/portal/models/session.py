import os

from gi.repository import GObject

from ...common.logger import logger
from ...common.scanner import Scanner, Description
from ...common.utils import get_projects_path, valid_project, valid_file


class Session(GObject.GObject):
    __gsignals__ = {
        "found": (GObject.SignalFlags.RUN_LAST, None, (object,)),
    }

    def scan(self) -> None:
        scanner = Scanner(path=get_projects_path())
        scanner.connect("found", self.__on_scanner_found)
        scanner.scan()

    def __on_scanner_found(self, scanner: Scanner, path: str) -> None:
        if not valid_project(path):
            return

        summary_path = os.path.join(path, "gameeky.project")

        if not valid_file(summary_path):
            return

        logger.debug(f"Found {summary_path}")
        description = Description.new_from_json(summary_path)

        self.emit("found", description)
