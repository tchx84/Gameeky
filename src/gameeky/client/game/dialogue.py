# Copyright (c) 2024 Martín Abente Lahaye.
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

from .service import Service

from ...common.logger import logger
from ...common.dialogue import Dialogue as CommonDialogue


class Dialogue(CommonDialogue, GObject.GObject):
    __gsignals__ = {
        "updated": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    def __init__(self, service: Service) -> None:
        CommonDialogue.__init__(self)
        GObject.GObject.__init__(self)

        self._service = service

        self._updated_source_id: Optional[int] = None
        self._registered_source_id: Optional[int] = self._service.connect(
            "registered",
            self.__on_registered,
        )

    def __on_registered(self, *args) -> None:
        self._updated_source_id = self._service.connect(
            "dialogue-updated",
            self.__on_updated,
        )

    def __on_updated(self, service: Service, dialogue: CommonDialogue) -> None:
        GLib.idle_add(self.__run_on_main_thread, dialogue)

    def __run_on_main_thread(self, dialogue: CommonDialogue) -> None:
        self.text = dialogue.text

        self.emit("updated")

    def shutdown(self) -> None:
        if self._updated_source_id is not None:
            self._service.disconnect(self._updated_source_id)

        if self._registered_source_id is not None:
            self._service.disconnect(self._registered_source_id)

        self._updated_source_id = None
        self._registered_source_id = None

        logger.debug("Client.Dialogue.shut")
