#!/usr/bin/python

import sys
import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gio, Gtk, GLib

from valley.client.game.service import Service
from valley.client.game.scene import Scene as SceneModel
from valley.client.graphics.scene import Scene as SceneView
from valley.client.input.keyboard import Keyboard

from valley.common.command import Command
from valley.common.definitions import (
    TILES_X,
    TILES_Y,
)
from valley.common.definitions import (
    DEFAULT_ADDRESS,
    DEFAULT_SESSION_PORT,
    DEFAULT_MESSAGES_PORT,
    DEFAULT_SCENE_PORT,
)


class Window(Gtk.ApplicationWindow):
    def __init__(self, application: Gtk.Application, model: SceneModel) -> None:
        super().__init__(application=application)

        self.set_title("Valley")

        self._ratio = Gtk.AspectFrame()
        self._ratio.set_obey_child(False)
        self._ratio.set_ratio(TILES_X / TILES_Y)

        self._view = SceneView(model=model)
        self._view.set_vexpand(True)
        self._view.set_hexpand(True)

        self._ratio.set_child(self._view)
        self.set_child(self._ratio)


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
            context=GLib.MainContext.default(),
        )
        self._service.register()

        self._model = SceneModel(
            width=TILES_X,
            height=TILES_Y,
            service=self._service,
        )

    def _setup_graphics(self) -> None:
        self._window = Window(application=self, model=self._model)
        self._window.present()

    def _setup_input(self) -> None:
        self._input = Keyboard(widget=self._window, service=self._service)

    def do_activate(self) -> None:
        self._setup_game()
        self._setup_graphics()
        self._setup_input()

    def do_command_line(self, command_line: Gio.ApplicationCommandLine) -> int:
        options = command_line.get_options_dict().end().unpack()

        self._address = options.get(Command.ADDRESS, DEFAULT_ADDRESS)
        self._session_port = options.get(Command.SESSION_PORT, DEFAULT_SESSION_PORT)
        self._messages_port = options.get(Command.MESSAGES_PORT, DEFAULT_MESSAGES_PORT)
        self._scene_port = options.get(Command.SCENE_PORT, DEFAULT_SCENE_PORT)

        self.do_activate()
        return 0

    def do_shutdown(self) -> None:
        self._service.unregister()
        Gtk.Application.do_shutdown(self)


if __name__ == "__main__":
    application = Application()
    application.run(sys.argv)
