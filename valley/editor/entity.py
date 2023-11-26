#!/usr/bin/python

import sys
import gi
import os

__dir__ = os.path.dirname(os.path.abspath(__file__))

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from typing import Any, Optional

from gi.repository import Gio, Adw, Gdk, Gtk

from .widgets.entity_window import EntityWindow
from .widgets.entity_new_window import EntityNewWindow
from .widgets.entity_open_window import EntityOpenWindow

from ..common.logger import logger
from ..common.utils import get_data_path, set_data_path, get_data_folder
from ..common.definitions import Format
from ..common.scanner import Scanner, Description

from ..server.game.actuators.base import ActuatorRegistry


class Application(Adw.Application):
    def __init__(self) -> None:
        super().__init__(
            application_id="dev.tchx84.valley.editor.Entity",
            flags=Gio.ApplicationFlags.NON_UNIQUE,
        )

    def __on_new(self, action: Gio.SimpleAction, data: Optional[Any] = None) -> None:
        dialog = EntityNewWindow(transient_for=self._window)
        dialog.connect("done", self.__on_done)
        dialog.present()

    def __on_open(self, action: Gio.SimpleAction, data: Optional[Any] = None) -> None:
        dialog = EntityOpenWindow(transient_for=self._window)
        dialog.connect("done", self.__on_done)
        dialog.present()

    def __on_done(self, dialog: EntityOpenWindow) -> None:
        if (description := dialog.description) is None:
            return

        ActuatorRegistry.reset()

        scanner = Scanner(path=get_data_path("actuators"))
        scanner.connect("found", self.__on_scanner_found)
        scanner.connect("done", self.__on_scanner_done, dialog.data_path, description)
        scanner.scan()

    def __on_scanner_found(self, scanner: Scanner, path: str) -> None:
        ActuatorRegistry.register(path)

    def __on_scanner_done(
        self,
        scanner: Scanner,
        data_path: str,
        description: Description,
    ) -> None:
        set_data_path(data_path)
        self._window.description = description

    def __on_save(self, action: Gio.SimpleAction, data: Optional[Any] = None) -> None:
        folder = get_data_folder("entities")

        json_filter = Gtk.FileFilter()
        json_filter.add_pattern(f"*.{Format.ENTITY}")

        dialog = Gtk.FileDialog()
        dialog.props.initial_folder = folder
        dialog.props.initial_name = self._window.suggested_name
        dialog.props.default_filter = json_filter
        dialog.save(callback=self.__on_save_finished)

    def __on_save_finished(
        self,
        dialog: Gtk.FileDialog,
        result: Gio.AsyncResult,
    ) -> None:
        try:
            file = dialog.save_finish(result)
        except Exception as e:
            logger.error(e)
            return

        file = Gio.File.new_for_path(file.get_path())
        file.replace_contents(
            contents=self._window.description.to_json().encode("UTF-8"),
            etag=None,
            make_backup=False,
            flags=Gio.FileCreateFlags.REPLACE_DESTINATION,
            cancellable=None,
        )

    def do_activate(self) -> None:
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(os.path.join(__dir__, "style.css"))
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

        self._window = EntityWindow(application=self)
        self._window.present()

    def do_startup(self) -> None:
        Adw.Application.do_startup(self)

        new_action = Gio.SimpleAction.new("new", None)
        new_action.connect("activate", self.__on_new)
        self.add_action(new_action)

        open_action = Gio.SimpleAction.new("open", None)
        open_action.connect("activate", self.__on_open)
        self.add_action(open_action)

        save_action = Gio.SimpleAction.new("save", None)
        save_action.connect("activate", self.__on_save)
        self.add_action(save_action)

    def do_shutdown(self) -> None:
        Adw.Application.do_shutdown(self)


def main() -> None:
    application = Application()
    application.run(sys.argv)
