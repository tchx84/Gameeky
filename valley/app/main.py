#!/usr/bin/python

import os
import sys
import gi

__dir__ = os.path.dirname(os.path.abspath(__file__))

gi.require_version("Gdk", "4.0")
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gdk, Gtk, Gio, Adw

from typing import Any, Optional

from .widgets.window import Window
from .widgets.session_new_window import SessionNewWindow
from .widgets.session_join_window import SessionJoinWindow
from .models.session_host import SessionHost
from .models.session_guest import SessionGuest

from ..common.logger import logger
from ..common.scanner import Description
from ..common.monitor import Monitor


class Application(Adw.Application):
    def __init__(self) -> None:
        super().__init__(
            application_id="dev.tchx84.valley.Client",
            flags=Gio.ApplicationFlags.NON_UNIQUE,
        )
        self._monitor = Monitor.default()
        self._session_host: Optional[SessionHost] = None
        self._session_guest: Optional[SessionGuest] = None
        self._description: Optional[Description] = None

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
        if self._session_guest is not None:
            self._session_guest.shutdown()

    def _shutdown_host(self) -> None:
        if self._session_host is not None:
            self._session_host.shutdown()

    def _start_host(self) -> None:
        if self._description is None:
            return

        self._session_host = SessionHost(
            data_path=self._description.data_path,
            scene=self._description.scene_path,
            clients=self._description.clients,
            session_port=self._description.session_port,
            messages_port=self._description.messages_port,
            scene_port=self._description.scene_port,
            stats_port=self._description.stats_port,
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
            data_path=self._description.data_path,
            address=self._description.address,
            session_port=self._description.session_port,
            messages_port=self._description.messages_port,
            scene_port=self._description.scene_port,
            stats_port=self._description.stats_port,
            widget=self._window,
        )

        self._session_guest.connect("started", self.__on_guest_started)
        self._session_guest.connect("initializing", self.__on_session_initializing)
        self._session_guest.connect("failed", self.__on_session_failed)
        self._session_guest.start()

    def __on_guest_started(self, session: SessionGuest) -> None:
        self._window.switch_to_game(session.scene, session.stats)

    def __on_session_initializing(self, *args) -> None:
        self._window.switch_to_loading()

    def __on_session_failed(self, *args) -> None:
        self._window.switch_to_failed()

    def do_activate(self) -> None:
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(os.path.join(__dir__, "style.css"))
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

        self._window = Window(application=self)
        self._window.connect("reload", self.__on_reload)
        self._window.present()

    def do_startup(self) -> None:
        Adw.Application.do_startup(self)

        new_action = Gio.SimpleAction.new("new", None)
        new_action.connect("activate", self.__on_new)
        self.add_action(new_action)

        join_action = Gio.SimpleAction.new("join", None)
        join_action.connect("activate", self.__on_join)
        self.add_action(join_action)

    def do_shutdown(self) -> None:
        self._monitor.shutdown()
        self._shutdown_guest()
        self._shutdown_host()
        Adw.Application.do_shutdown(self)

        logger.info("Client.Application.shut")


def main() -> None:
    application = Application()
    application.run(sys.argv)
