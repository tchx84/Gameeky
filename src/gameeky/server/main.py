#!/usr/bin/python

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
    DEFAULT_MESSAGES_PORT,
    DEFAULT_SCENE_PORT,
    DEFAULT_STATS_PORT,
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
            Command.MESSAGES_PORT,
            ord("u"),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.INT,
            "Port to be used for the updates service",
            None,
        )
        self.add_main_option(
            Command.SCENE_PORT,
            ord("e"),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.INT,
            "Port to be used for the scene service",
            None,
        )
        self.add_main_option(
            Command.STATS_PORT,
            ord("t"),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.INT,
            "Port to be used for the stats service",
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
            messages_port=self._messages_port,
            scene_port=self._scene_port,
            stats_port=self._stats_port,
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
        self._messages_port = options.get(Command.MESSAGES_PORT, DEFAULT_MESSAGES_PORT)
        self._scene_port = options.get(Command.SCENE_PORT, DEFAULT_SCENE_PORT)
        self._stats_port = options.get(Command.STATS_PORT, DEFAULT_STATS_PORT)

        self.do_activate()
        return 0

    def do_shutdown(self) -> None:
        self._service.shutdown()
        Gio.Application.do_shutdown(self)


if __name__ == "__main__":
    application = Application()
    application.run(sys.argv)
