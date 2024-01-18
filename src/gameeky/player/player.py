#!/usr/bin/python
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
import time
import gi

gi.require_version("Gdk", "4.0")
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from typing import Any, Optional
from gettext import gettext as _

from gi.repository import Gdk, Gtk, GLib, Gio, Adw

from .widgets.window import Window
from .widgets.session_new_window import SessionNewWindow
from .widgets.session_join_window import SessionJoinWindow
from .models.session_host import SessionHost
from .models.session_guest import SessionGuest

from ..common.logger import logger
from ..common.scanner import Description
from ..common.monitor import Monitor
from ..common.widgets.about_window import present_about
from ..common.utils import (
    get_project_folder,
    set_project_path,
    find_project_path,
    bytearray_to_string,
)
from ..common.definitions import (
    Command,
    Format,
    DEFAULT_ADDRESS,
    DEFAULT_CLIENTS,
    DEFAULT_SESSION_PORT,
    DEFAULT_MESSAGES_PORT,
)


class Application(Adw.Application):
    def __init__(self) -> None:
        super().__init__(
            application_id="dev.tchx84.Gameeky.Player",
            flags=Gio.ApplicationFlags.NON_UNIQUE
            | Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
        )
        GLib.set_application_name(_("Player"))

        self._monitor = Monitor.default()
        self._session_host: Optional[SessionHost] = None
        self._session_guest: Optional[SessionGuest] = None
        self._description: Optional[Description] = None

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
        dialog = SessionNewWindow(transient_for=self._window)
        dialog.connect("done", self.__on_new_done)
        dialog.present()

    def __on_new_done(self, dialog: SessionNewWindow) -> None:
        self._description = dialog.description
        self._monitor.shutdown()
        self._shutdown_guest()
        self._shutdown_host()
        self._start_host()

    def __on_join(self, action: Gio.SimpleAction, data: Optional[Any] = None) -> None:
        dialog = SessionJoinWindow(transient_for=self._window)
        dialog.connect("done", self.__on_join_done)
        dialog.present()

    def __on_join_done(self, dialog: SessionNewWindow) -> None:
        self._description = dialog.description
        self._monitor.shutdown()
        self._shutdown_guest()
        self._shutdown_host()
        self._start_guest()

    def __on_reload(self, window: Window) -> None:
        self._monitor.shutdown()
        self._shutdown_guest()
        self._shutdown_host()
        self._start_host()

    def _shutdown_guest(self) -> None:
        self._window.scene = None
        self._window.stats = None
        self._window.dialogue = None

        if self._session_guest is not None:
            self._session_guest.shutdown()

        self._session_guest = None

    def _shutdown_host(self) -> None:
        if self._session_host is not None:
            self._session_host.shutdown()

        self._session_host = None

    def _start_host(self) -> None:
        if self._description is None:
            return

        self._session_host = SessionHost(
            project_path=self._description.project_path,
            scene=self._description.scene_path,
            clients=self._description.clients,
            session_port=self._description.session_port,
            messages_port=self._description.messages_port,
        )

        self._session_host.connect("started", self.__on_host_started)
        self._session_host.connect("initializing", self.__on_session_initializing)
        self._session_host.connect("failed", self.__on_session_failed)
        self._session_host.start()

    def __on_host_started(self, session: SessionHost) -> None:
        self._start_guest()

    def _start_guest(self) -> None:
        if self._description is None:
            return

        self._session_guest = SessionGuest(
            project_path=self._description.project_path,
            address=self._description.address,
            session_port=self._description.session_port,
            messages_port=self._description.messages_port,
            widget=self._window,
        )

        self._session_guest.connect("initializing", self.__on_session_initializing)
        self._session_guest.connect("started", self.__on_guest_started)
        self._session_guest.connect("failed", self.__on_session_failed)
        self._session_guest.start()

    def __on_guest_started(self, session: SessionGuest) -> None:
        self._window.scene = session.scene
        self._window.stats = session.stats
        self._window.dialogue = session.dialogue
        self._window.switch_to_game()

    def __on_session_initializing(self, *args) -> None:
        self._window.switch_to_loading()

    def __on_session_failed(self, *args) -> None:
        self._window.switch_to_failed()

    def __on_save(self, action: Gio.SimpleAction, data: Optional[Any] = None) -> None:
        if self._session_host is None:
            self._window.warn("Only an active host session can save the game state")
            return

        folder = get_project_folder("scenes")

        json_filter = Gtk.FileFilter()
        json_filter.add_pattern(f"*.{Format.SCENE}")

        initial_name = f"{self._session_host.scene_name}_{time.strftime('%Y%m%d-%H%M%S')}.{Format.SCENE}"

        dialog = Gtk.FileDialog()
        dialog.props.initial_folder = folder
        dialog.props.initial_name = initial_name
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

        if self._session_host is None:
            return

        self._session_host.request_description(
            self.__on_description_received,
            file.get_path(),
        )

    def __on_description_received(self, path: str, description: Description) -> None:
        file = Gio.File.new_for_path(path)
        file.replace_contents(
            contents=description.to_json().encode("UTF-8"),
            etag=None,
            make_backup=False,
            flags=Gio.FileCreateFlags.REPLACE_DESTINATION,
            cancellable=None,
        )

    def __on_about(self, action: Gio.SimpleAction, data: Optional[Any] = None) -> None:
        present_about(self._window)

    def do_command_line(self, command_line: Gio.ApplicationCommandLine) -> int:
        options = command_line.get_options_dict().end().unpack()

        if (project_path := options.get(Command.PROJECT_PATH, None)) is not None:
            set_project_path(project_path)

        if (scene_path := options.get(GLib.OPTION_REMAINING, None)) is not None:
            scene_path = bytearray_to_string(scene_path[-1])

            self._description = Description(
                address=DEFAULT_ADDRESS,
                project_path=find_project_path(scene_path),
                scene_path=scene_path,
                clients=DEFAULT_CLIENTS,
                session_port=DEFAULT_SESSION_PORT,
                messages_port=DEFAULT_MESSAGES_PORT,
            )

        self.activate()
        return 0

    def do_activate(self) -> None:
        css_provider = Gtk.CssProvider()
        css_provider.load_from_resource("/dev/tchx84/gameeky/player/style.css")
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

        self._window = Window(application=self)
        self._window.connect("reload", self.__on_reload)
        self._window.present()

        self._start_host()

    def do_startup(self) -> None:
        Adw.Application.do_startup(self)

        new_action = Gio.SimpleAction.new("new", None)
        new_action.connect("activate", self.__on_new)
        self.add_action(new_action)

        join_action = Gio.SimpleAction.new("join", None)
        join_action.connect("activate", self.__on_join)
        self.add_action(join_action)

        save_action = Gio.SimpleAction.new("save", None)
        save_action.connect("activate", self.__on_save)
        self.add_action(save_action)

        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.__on_about)
        self.add_action(about_action)

    def do_shutdown(self) -> None:
        self._monitor.shutdown()
        self._shutdown_guest()
        self._shutdown_host()
        Adw.Application.do_shutdown(self)

        logger.debug("Client.Application.shut")


def main(version: str) -> None:
    application = Application()
    application.run(sys.argv)
