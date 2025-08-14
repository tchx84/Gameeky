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

from .utils import set_session_project

from .widgets.window import Window
from .widgets.session_settings_window import SessionSettingsWindow

from ..common.logger import logger
from ..common.monitor import Monitor
from ..common.utils import bytearray_to_string
from ..common.definitions import Command
from ..common.widgets.about_window import present_about
from ..common.widgets.documentation_wrapper import present_documentation
from ..common.widgets.confirmation_save_window import ConfirmationSaveWindow


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
        self._pending_changes = False
        self._monitor = Monitor.default()

        self.add_main_option(
            Command.PROJECT_PATH,
            ord("d"),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.STRING,
            "The absolute path to the project",
            None,
        )

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
        self.source_path = None

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
            self.source_path = path

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
        self.source_path = path
        self._pending_changes = False

    def __on_reload(self, window: Window, data: Optional[Any] = None) -> None:
        if self._window is None:
            return
        if self._source_path is None:
            return

        self._window.source = self._do_load(self._source_path)

    def _do_load(self, path: str) -> str:
        file = Gio.File.new_for_path(path)
        success, contents, _ = file.load_contents(None)

        if success is False:
            return ""

        return contents.decode()

    def _on_changed(self, window: Window) -> None:
        self._pending_changes = True

    def __on_closed(self, window: Window) -> bool:
        if not self._pending_changes:
            return False

        dialog = ConfirmationSaveWindow(transient_for=self._window)
        dialog.connect("saved", self.__on_save)
        dialog.connect("discarded", self.__on_discarded)
        dialog.present()

        return True

    def __on_discarded(self, dialog: ConfirmationSaveWindow) -> None:
        if self._window is None:
            return

        self._pending_changes = False
        self._window.close()

    def __on_edit(self, action: Gio.SimpleAction, data: Optional[Any] = None) -> None:
        dialog = SessionSettingsWindow(transient_for=self._window)
        dialog.present()

    def __on_about(self, action: Gio.SimpleAction, data: Optional[Any] = None) -> None:
        present_about(self._window)

    def __on_documentation(
        self,
        action: Gio.SimpleAction,
        data: Optional[Any] = None,
    ) -> None:
        present_documentation(self._window)

    def do_command_line(self, command_line: Gio.ApplicationCommandLine) -> int:
        options = command_line.get_options_dict().end().unpack()

        if (project_path := options.get(Command.PROJECT_PATH, None)) is not None:
            set_session_project(project_path)

        if (source_path := options.get(GLib.OPTION_REMAINING, None)) is not None:
            source_path = bytearray_to_string(source_path[-1])
            self.source_path = source_path

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
        self._window.connect("changed", self._on_changed)
        self._window.connect("reload", self.__on_reload)
        self._window.connect("close-request", self.__on_closed)
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

        edit_action = Gio.SimpleAction.new("edit", None)
        edit_action.connect("activate", self.__on_edit)
        self.add_action(edit_action)

        documentation_action = Gio.SimpleAction.new("documentation", None)
        documentation_action.connect("activate", self.__on_documentation)
        self.add_action(documentation_action)

        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.__on_about)
        self.add_action(about_action)

    def do_shutdown(self) -> None:
        self._monitor.shutdown()
        Adw.Application.do_shutdown(self)

    @property
    def source_path(self) -> Optional[str]:
        return self._source_path

    @source_path.setter
    def source_path(self, path: Optional[str]) -> None:
        self._monitor.shutdown()
        self._source_path = path

        if self._source_path is not None:
            self._monitor.add(self._source_path)


def main(version: str) -> None:
    application = Application()
    application.run(sys.argv)
