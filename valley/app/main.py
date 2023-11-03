#!/usr/bin/python

import sys
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gio, Adw, GLib

from typing import Any, Optional

from .widgets.window import Window
from .models.session import Session

from ..common.definitions import (
    Command,
    DEFAULT_SCENE,
    DEFAULT_CLIENTS,
    DEFAULT_ADDRESS,
    DEFAULT_SESSION_PORT,
    DEFAULT_MESSAGES_PORT,
    DEFAULT_SCENE_PORT,
    DEFAULT_STATS_PORT,
)


class Application(Adw.Application):
    def __init__(self) -> None:
        super().__init__(
            application_id="dev.tchx84.valley.Client",
            flags=Gio.ApplicationFlags.NON_UNIQUE
            | Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
        )

        self._session: Optional[Session] = None

        self.add_main_option(
            Command.SCENE,
            ord("n"),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.STRING,
            "The relative path to the scene to be used",
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
        self.add_main_option(
            Command.SESSION_PORT,
            ord("s"),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.INT,
            "Port to connect to the session service",
            None,
        )
        self.add_main_option(
            Command.MESSAGES_PORT,
            ord("u"),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.INT,
            "Port to connect for the updates service",
            None,
        )
        self.add_main_option(
            Command.SCENE_PORT,
            ord("e"),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.INT,
            "Port to connect for the scene service",
            None,
        )
        self.add_main_option(
            Command.STATS_PORT,
            ord("t"),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.INT,
            "Port to connect for the stats service",
            None,
        )
        self.add_main_option(
            Command.ADDRESS,
            ord("a"),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.STRING,
            "The IPv4 address for the game server",
            None,
        )

    def __on_create(self, action: Gio.SimpleAction, data: Optional[Any] = None) -> None:
        self._setup_session(host=True)

    def __on_join(self, action: Gio.SimpleAction, data: Optional[Any] = None) -> None:
        self._setup_session(host=False)

    def __on_session_initializing(self, session: Session) -> None:
        self._window.switch_to_loading()

    def __on_session_started(self, session: Session) -> None:
        self._window.switch_to_game(session.scene, session.stats)

    def _setup_session(self, host: bool) -> None:
        self._session = Session(
            scene=self._scene,
            clients=self._clients,
            address=self._address,
            session_port=self._session_port,
            messages_port=self._messages_port,
            scene_port=self._scene_port,
            stats_port=self._stats_port,
            window=self._window,
            host=host,
        )
        self._session.connect("initializing", self.__on_session_initializing)
        self._session.connect("started", self.__on_session_started)
        self._session.create()

    def do_activate(self) -> None:
        self._window = Window(application=self)
        self._window.present()

    def do_startup(self) -> None:
        Adw.Application.do_startup(self)

        create_action = Gio.SimpleAction.new("create", None)
        create_action.connect("activate", self.__on_create)
        self.add_action(create_action)

        join_action = Gio.SimpleAction.new("join", None)
        join_action.connect("activate", self.__on_join)
        self.add_action(join_action)

    def do_command_line(self, command_line: Gio.ApplicationCommandLine) -> int:
        options = command_line.get_options_dict().end().unpack()

        self._scene = options.get(Command.SCENE, DEFAULT_SCENE)
        self._clients = options.get(Command.CLIENTS, DEFAULT_CLIENTS)
        self._address = options.get(Command.ADDRESS, DEFAULT_ADDRESS)
        self._session_port = options.get(Command.SESSION_PORT, DEFAULT_SESSION_PORT)
        self._messages_port = options.get(Command.MESSAGES_PORT, DEFAULT_MESSAGES_PORT)
        self._scene_port = options.get(Command.SCENE_PORT, DEFAULT_SCENE_PORT)
        self._stats_port = options.get(Command.SCENE_PORT, DEFAULT_STATS_PORT)

        self.do_activate()
        return 0

    def do_shutdown(self) -> None:
        if self._session is not None:
            self._session.shutdown()

        Adw.Application.do_shutdown(self)


def main() -> None:
    application = Application()
    application.run(sys.argv)
