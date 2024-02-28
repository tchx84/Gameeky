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
import gi

gi.require_version("Gdk", "4.0")
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from typing import Any, Optional
from gettext import gettext as _

from gi.repository import Gdk, Gio, Gtk, GLib, Adw

from .widgets.scene_window import SceneWindow
from .widgets.scene_new_window import SceneNewWindow
from .widgets.scene_open_window import SceneOpenWindow
from .widgets.scene_edit_window import SceneEditWindow
from .widgets.confirmation_save_window import ConfirmationSaveWindow
from .models.scene import Scene as SceneModel
from .models.scene_session import Session as SessionModel

from ..common.logger import logger
from ..common.scanner import Description
from ..common.definitions import Command, Format
from ..common.monitor import Monitor
from ..common.widgets.about_window import present_about
from ..common.widgets.documentation_wrapper import present_documentation
from ..common.utils import (
    set_project_path,
    get_project_folder,
    find_project_path,
    bytearray_to_string,
    launch_player,
)


class Application(Adw.Application):
    def __init__(self) -> None:
        super().__init__(
            application_id="dev.tchx84.Gameeky.Scene",
            flags=Gio.ApplicationFlags.NON_UNIQUE
            | Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
        )
        GLib.set_application_name(_("Scene Editor"))

        self._monitor = Monitor.default()
        self._project_path: Optional[str] = None
        self._scene_path: Optional[str] = None
        self._description: Optional[Description] = None
        self._pending_changes = False

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
            "The absolute path to the scene",
            None,
        )

    def __on_new(self, action: Gio.SimpleAction, data: Optional[Any] = None) -> None:
        dialog = SceneNewWindow(transient_for=self._window)
        dialog.connect("done", self.__on_done)
        dialog.present()

    def __on_open(self, action: Gio.SimpleAction, data: Optional[Any] = None) -> None:
        dialog = SceneOpenWindow(transient_for=self._window)
        dialog.connect("done", self.__on_done)
        dialog.present()

    def __on_edit(self, action: Gio.SimpleAction, data: Optional[Any] = None) -> None:
        dialog = SceneEditWindow(
            transient_for=self._window,
            scene_path=self._scene_path,
        )
        dialog.connect("done", self.__on_edit_done)
        dialog.description = self._window.description
        dialog.present()

    def __on_edit_done(self, dialog: SceneEditWindow) -> None:
        self._pending_changes = True
        self.__on_done(dialog)

    def __on_done(self, dialog: SceneNewWindow) -> None:
        if (description := dialog.description) is None:
            return

        self._project_path = dialog.project_path
        self._scene_path = dialog.scene_path
        self._description = description
        self._start_session()

    def _on_reload(self, window: SceneWindow) -> None:
        self._description = self._window.description
        self._start_session()

    def _on_changed(self, window: SceneWindow) -> None:
        self._pending_changes = True

    def _on_committed(self, window: SceneWindow) -> None:
        if self._scene_path is not None:
            self._do_save(self._scene_path)

    def _start_session(self) -> None:
        if self._project_path is None:
            return
        if self._description is None:
            return

        set_project_path(self._project_path)

        self._window.reset()

        self._session_model = SessionModel()
        self._session_model.connect("registered", self.__on_session_registered)
        self._session_model.connect("ready", self.__on_session_ready)
        self._session_model.scan()

    def __on_session_registered(
        self,
        model: SessionModel,
        description: Description,
    ) -> None:
        self._window.register(description)

    def __on_session_ready(
        self,
        model: SessionModel,
    ) -> None:
        if self._description is not None:
            self._window.description = self._description

    def __on_save(self, *args) -> None:
        if self._scene_path is None:
            self.__on_save_as()
        else:
            self._do_save(self._scene_path)

    def __on_save_as(self, *args) -> None:
        folder = get_project_folder("scenes")

        json_filter = Gtk.FileFilter()
        json_filter.add_pattern(f"*.{Format.SCENE}")

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
        else:
            self._do_save(file.get_path())

    def _do_save(self, path) -> None:
        file = Gio.File.new_for_path(path)
        file.replace_contents(
            contents=self._window.description.to_json().encode("UTF-8"),
            etag=None,
            make_backup=False,
            flags=Gio.FileCreateFlags.REPLACE_DESTINATION,
            cancellable=None,
        )
        self._scene_path = path
        self._pending_changes = False

    def __on_try(self, action: Gio.SimpleAction, data: Optional[Any] = None) -> None:
        if self._scene_path is None:
            self.__on_save_as()
        else:
            self._do_save(self._scene_path)
            self._try_scene()

    def _try_scene(self) -> None:
        if self._project_path is None:
            return
        if self._scene_path is None:
            return

        launch_player(self._project_path, self._scene_path)

    def __on_about(self, action: Gio.SimpleAction, data: Optional[Any] = None) -> None:
        present_about(self._window)

    def __on_documentation(
        self,
        action: Gio.SimpleAction,
        data: Optional[Any] = None,
    ) -> None:
        present_documentation(self._window)

    def __on_close_requested(self, window: SceneWindow) -> bool:
        if not self._pending_changes:
            return False

        dialog = ConfirmationSaveWindow(transient_for=self._window)
        dialog.connect("saved", self.__on_save)
        dialog.connect("discarded", self.__on_discarded)
        dialog.present()

        return True

    def __on_discarded(self, dialog: ConfirmationSaveWindow) -> None:
        self.quit()

    def do_command_line(self, command_line: Gio.ApplicationCommandLine) -> int:
        options = command_line.get_options_dict().end().unpack()

        if (project_path := options.get(Command.PROJECT_PATH, None)) is not None:
            set_project_path(project_path)

        if (scene_path := options.get(GLib.OPTION_REMAINING, None)) is not None:
            scene_path = bytearray_to_string(scene_path[-1])

            self._project_path = find_project_path(scene_path)
            self._scene_path = scene_path
            self._description = SceneModel.new_from_file(self._project_path, scene_path)

        self.activate()
        return 0

    def do_activate(self) -> None:
        css_provider = Gtk.CssProvider()
        css_provider.load_from_resource("/dev/tchx84/gameeky/editor/style.css")
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

        self._window = SceneWindow(application=self)
        self._window.connect("reload", self._on_reload)
        self._window.connect("changed", self._on_changed)
        self._window.connect("committed", self._on_committed)
        self._window.connect("close-request", self.__on_close_requested)
        self._window.present()

        self._start_session()

    def do_startup(self) -> None:
        Adw.Application.do_startup(self)

        new_action = Gio.SimpleAction.new("new", None)
        new_action.connect("activate", self.__on_new)
        self.add_action(new_action)

        open_action = Gio.SimpleAction.new("open", None)
        open_action.connect("activate", self.__on_open)
        self.add_action(open_action)

        edit_action = Gio.SimpleAction.new("edit", None)
        edit_action.connect("activate", self.__on_edit)
        self.add_action(edit_action)

        save_action = Gio.SimpleAction.new("save", None)
        save_action.connect("activate", self.__on_save)
        self.add_action(save_action)

        save_as_action = Gio.SimpleAction.new("save_as", None)
        save_as_action.connect("activate", self.__on_save_as)
        self.add_action(save_as_action)

        try_action = Gio.SimpleAction.new("try", None)
        try_action.connect("activate", self.__on_try)
        self.add_action(try_action)

        documentation_action = Gio.SimpleAction.new("documentation", None)
        documentation_action.connect("activate", self.__on_documentation)
        self.add_action(documentation_action)

        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.__on_about)
        self.add_action(about_action)

    def do_shutdown(self) -> None:
        self._monitor.shutdown()
        Adw.Application.do_shutdown(self)


def main(version: str) -> None:
    application = Application()
    application.run(sys.argv)
