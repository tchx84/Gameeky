#!/usr/bin/python
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


import sys

from gi.repository import Gio, GLib

from gameeky.server.game.service import Service
from gameeky.server.game.entity import EntityRegistry
from gameeky.server.game.actuators.base import ActuatorRegistry
from gameeky.common.scanner import Scanner, Description
from gameeky.common.utils import get_project_path
from gameeky.common.definitions import (
    Command,
    DEFAULT_SCENE,
    DEFAULT_CLIENTS,
    DEFAULT_SESSION_PORT,
)


class Application(Gio.Application):
    def __init__(self) -> None:
        super().__init__(
            application_id="dev.tchx84.Gameeky.Server",
            flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
        )

        self.add_main_option(
            Command.SCENE,
            ord("n"),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.STRING,
            "The relative path to the scene to be used",
            None,
        )
        self.add_main_option(
            Command.SESSION_PORT,
            ord("s"),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.INT,
            "Port to be used for the session service",
            None,
        )
        self.add_main_option(
            Command.CLIENTS,
            ord("c"),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.INT,
            "The number of clients that are allowed to join",
            None,
        )

    def __on_entities_scanner_found(self, scanner: Scanner, path: str) -> None:
        EntityRegistry.register(Description.new_from_json(path))

    def __on_entities_scanner_done(self, scanner: Scanner) -> None:
        scanner = Scanner(get_project_path("actuators"))
        scanner.connect("found", self.__on_actuators_scanner_found)
        scanner.connect("done", self.__on_actuators_scanner_done)
        scanner.scan()

    def __on_actuators_scanner_found(self, scanner: Scanner, path: str) -> None:
        ActuatorRegistry.register(path)

    def __on_actuators_scanner_done(self, scanner: Scanner) -> None:
        self._service = Service(
            scene=self._scene,
            clients=self._clients,
            session_port=self._session_port,
            context=GLib.MainContext.default(),
        )

    def do_activate(self) -> None:
        scanner = Scanner(get_project_path("entities"))
        scanner.connect("found", self.__on_entities_scanner_found)
        scanner.connect("done", self.__on_entities_scanner_done)
        scanner.scan()

        self.hold()

        Gio.Application.do_activate(self)

    def do_command_line(self, command_line: Gio.ApplicationCommandLine) -> int:
        options = command_line.get_options_dict().end().unpack()

        self._scene = options.get(Command.SCENE, DEFAULT_SCENE)
        self._clients = options.get(Command.CLIENTS, DEFAULT_CLIENTS)
        self._session_port = options.get(Command.SESSION_PORT, DEFAULT_SESSION_PORT)

        self.do_activate()
        return 0

    def do_shutdown(self) -> None:
        self._service.shutdown()
        Gio.Application.do_shutdown(self)


if __name__ == "__main__":
    application = Application()
    application.run(sys.argv)
