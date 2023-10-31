#!/usr/bin/python

import sys
import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gio, Gtk, GLib

from .widgets.window import Window

from ..game.service import Service
from ..game.scene import Scene as SceneModel
from ..graphics.entity import EntityRegistry as EntityGraphicsRegistry
from ..input.keyboard import Keyboard
from ..sound.entity import EntityRegistry as EntitySoundRegistry
from ..sound.scene import Scene as ScenePlayer

from ...common.utils import get_data_path
from ...common.scanner import Scanner, Description
from ...common.definitions import (
    Command,
    TILES_X,
    TILES_Y,
    DEFAULT_ADDRESS,
    DEFAULT_SESSION_PORT,
    DEFAULT_MESSAGES_PORT,
    DEFAULT_SCENE_PORT,
    DEFAULT_STATS_PORT,
)


class Application(Gtk.Application):
    def __init__(self) -> None:
        super().__init__(
            application_id="dev.tchx84.valley.Client",
            flags=Gio.ApplicationFlags.NON_UNIQUE
            | Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
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

    def _setup_game(self) -> None:
        self._service = Service(
            address=self._address,
            session_port=self._session_port,
            messages_port=self._messages_port,
            scene_port=self._scene_port,
            stats_port=self._stats_port,
            context=GLib.MainContext.default(),
        )

        self._model = SceneModel(
            width=TILES_X,
            height=TILES_Y,
            service=self._service,
        )

        self._scanner = Scanner(path=get_data_path("entities"))
        self._scanner.connect("found", self.__on_scanner_found)
        self._scanner.connect("done", self.__on_scanner_done)
        self._scanner.scan()

    def __on_scanner_found(self, scanner: Scanner, description: Description) -> None:
        EntityGraphicsRegistry.register(description)
        EntitySoundRegistry.register(description)

    def __on_scanner_done(self, scanner: Scanner) -> None:
        self._service.register()

    def _setup_graphics(self) -> None:
        self._window = Window(application=self, model=self._model)
        self._window.present()

    def _setup_input(self) -> None:
        self._input = Keyboard(widget=self._window, service=self._service)

    def _setup_sound(self) -> None:
        self._player = ScenePlayer(model=self._model)

    def do_activate(self) -> None:
        self._setup_game()
        self._setup_graphics()
        self._setup_input()
        self._setup_sound()

    def do_command_line(self, command_line: Gio.ApplicationCommandLine) -> int:
        options = command_line.get_options_dict().end().unpack()

        self._address = options.get(Command.ADDRESS, DEFAULT_ADDRESS)
        self._session_port = options.get(Command.SESSION_PORT, DEFAULT_SESSION_PORT)
        self._messages_port = options.get(Command.MESSAGES_PORT, DEFAULT_MESSAGES_PORT)
        self._scene_port = options.get(Command.SCENE_PORT, DEFAULT_SCENE_PORT)
        self._stats_port = options.get(Command.SCENE_PORT, DEFAULT_STATS_PORT)

        self.do_activate()
        return 0

    def do_shutdown(self) -> None:
        self._service.unregister()
        Gtk.Application.do_shutdown(self)


def main() -> None:
    application = Application()
    application.run(sys.argv)
