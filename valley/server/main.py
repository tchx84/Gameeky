#!/usr/bin/python

import sys

from gi.repository import Gio, GLib

from valley.server.game.service import Service
from valley.common.command import Command
from valley.common.definitions import (
    DEFAULT_CLIENTS,
    DEFAULT_SESSION_PORT,
    DEFAULT_UPDATES_PORT,
    DEFAULT_SCENE_PORT,
)


class Application(Gio.Application):
    def __init__(self) -> None:
        super().__init__(
            application_id="dev.tchx84.valley.Server",
            flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
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
            Command.UPDATES_PORT,
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
            Command.CLIENTS,
            ord("c"),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.INT,
            "The number of clients that are allowed to join",
            None,
        )

    def do_activate(self) -> None:
        self._service = Service(
            clients=self._clients,
            session_port=self._session_port,
            updates_port=self._updates_port,
            scene_port=self._scene_port,
            context=GLib.MainContext.default(),
        )

        self.hold()

        Gio.Application.do_activate(self)

    def do_command_line(self, command_line: Gio.ApplicationCommandLine) -> int:
        options = command_line.get_options_dict().end().unpack()

        self._clients = options.get(Command.CLIENTS, DEFAULT_CLIENTS)
        self._session_port = options.get(Command.SESSION_PORT, DEFAULT_SESSION_PORT)
        self._updates_port = options.get(Command.UPDATES_PORT, DEFAULT_UPDATES_PORT)
        self._scene_port = options.get(Command.SCENE_PORT, DEFAULT_SCENE_PORT)

        self.do_activate()
        return 0

    def do_shutdown(self) -> None:
        Gio.Application.do_shutdown(self)


if __name__ == "__main__":
    application = Application()
    application.run(sys.argv)
