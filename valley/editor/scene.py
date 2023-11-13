#!/usr/bin/python

import sys
import gi
import os

__dir__ = os.path.dirname(os.path.abspath(__file__))

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gio, Adw

from .widgets.scene_window import SceneWindow


class Application(Adw.Application):
    def __init__(self) -> None:
        super().__init__(
            application_id="dev.tchx84.valley.editor.Scene",
            flags=Gio.ApplicationFlags.NON_UNIQUE,
        )

    def do_activate(self) -> None:
        self._window = SceneWindow(application=self)
        self._window.present()

    def do_startup(self) -> None:
        Adw.Application.do_startup(self)

    def do_shutdown(self) -> None:
        Adw.Application.do_shutdown(self)


def main() -> None:
    application = Application()
    application.run(sys.argv)
