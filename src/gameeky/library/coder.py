#!/usr/bin/python
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


import sys
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from typing import Any, Optional
from gettext import gettext as _

from gi.repository import GLib, Gio, Adw, Gdk, Gtk

from .widgets.window import Window

from ..common.logger import logger
from ..common.utils import bytearray_to_string


class Application(Adw.Application):
    def __init__(self) -> None:
        super().__init__(
            application_id="dev.tchx84.Gameeky.Coder",
            flags=Gio.ApplicationFlags.NON_UNIQUE
            | Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
        )
        GLib.set_application_name(_("Coder"))

        self._window: Optional[Window] = None
        self._source_path: Optional[str] = None

        self.add_main_option(
            GLib.OPTION_REMAINING,
            ord("f"),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.FILENAME_ARRAY,
            "The absolute path to the source",
            None,
        )

    def __on_new(self, action: Gio.SimpleAction, data: Optional[Any] = None) -> None:
        if self._window is None:
            return

        self._window.source = ""
        self._source_path = None

    def __on_open(self, action: Gio.SimpleAction, data: Optional[Any] = None) -> None:
        default_filter = Gtk.FileFilter()
        default_filter.add_pattern("*.py")

        dialog = Gtk.FileDialog()
        dialog.props.default_filter = default_filter
        dialog.open(callback=self.__on_open_finished)

    def __on_open_finished(
        self,
        dialog: Gtk.FileDialog,
        result: Gio.AsyncResult,
    ) -> None:
        if self._window is None:
            return

        try:
            file = dialog.open_finish(result)
        except Exception as e:
            logger.error(e)
        else:
            path = file.get_path()
            self._window.source = self._do_load(path)
            self._source_path = path

    def __on_save(self, *args) -> None:
        if self._source_path is None:
            self.__on_save_as()
        else:
            self._do_save(self._source_path)

    def __on_save_as(self, *args) -> None:
        default_filter = Gtk.FileFilter()
        default_filter.add_pattern("*.py")

        dialog = Gtk.FileDialog()
        dialog.props.initial_name = _("untitled") + ".py"
        dialog.props.default_filter = default_filter
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
        else:
            self._do_save(file.get_path())

    def _do_save(self, path: str) -> None:
        if self._window is None:
            return

        file = Gio.File.new_for_path(path)
        file.replace_contents(
            contents=self._window.source.encode(),
            etag=None,
            make_backup=False,
            flags=Gio.FileCreateFlags.REPLACE_DESTINATION,
            cancellable=None,
        )
        self._source_path = path

    def _do_load(self, path: str) -> str:
        file = Gio.File.new_for_path(path)
        success, contents, _ = file.load_contents(None)

        if success is False:
            return ""

        return contents.decode()

    def do_command_line(self, command_line: Gio.ApplicationCommandLine) -> int:
        options = command_line.get_options_dict().end().unpack()

        if (source_path := options.get(GLib.OPTION_REMAINING, None)) is not None:
            source_path = bytearray_to_string(source_path[-1])

            self._source_path = source_path

        self.activate()
        return 0

    def do_activate(self) -> None:
        css_provider = Gtk.CssProvider()
        css_provider.load_from_resource("/dev/tchx84/gameeky/library/style.css")
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

        self._window = Window(application=self)
        self._window.present()

        if self._source_path is not None:
            self._window.source = self._do_load(self._source_path)

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

        save_as_action = Gio.SimpleAction.new("save_as", None)
        save_as_action.connect("activate", self.__on_save_as)
        self.add_action(save_as_action)

    def do_shutdown(self) -> None:
        Adw.Application.do_shutdown(self)


def main(version: str) -> None:
    application = Application()
    application.run(sys.argv)
