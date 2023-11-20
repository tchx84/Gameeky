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

from ..common.utils import wait
from ..common.logger import logger
from ..common.scanner import Description


class Application(Adw.Application):
    def __init__(self) -> None:
        super().__init__(
            application_id="dev.tchx84.valley.Client",
            flags=Gio.ApplicationFlags.NON_UNIQUE,
        )
        self._session_host: Optional[SessionHost] = None
        self._session_guest: Optional[SessionGuest] = None

    def __on_new(self, action: Gio.SimpleAction, data: Optional[Any] = None) -> None:
        dialog = SessionNewWindow(transient_for=self._window)
        dialog.connect("done", self.__on_new_done)
        dialog.present()

    def __on_new_done(self, dialog: SessionNewWindow) -> None:
        self._shutdown_guest()
        self._shutdown_host()
        self._start_host(dialog.description)

    def __on_join(self, action: Gio.SimpleAction, data: Optional[Any] = None) -> None:
        dialog = SessionJoinWindow(transient_for=self._window)
        dialog.connect("done", self.__on_join_done)
        dialog.present()

    def __on_join_done(self, dialog: SessionNewWindow) -> None:
        self._shutdown_guest()
        self._start_guest(dialog.description)

    def _shutdown_guest(self) -> None:
        if self._session_guest is not None:
            self._session_guest.shutdown()

            # XXX Switch to an asynchronous solution to prevent race condition
            # between the guest shutting down and the host shutting down...
            wait(milliseconds=250)

    def _shutdown_host(self) -> None:
        if self._session_host is not None:
            self._session_host.shutdown()

    def _start_host(self, description: Description) -> None:
        self._session_host = SessionHost(
            data_path=description.data_path,
            scene=description.scene_path,
            clients=description.clients,
            session_port=description.session_port,
            messages_port=description.messages_port,
            scene_port=description.scene_port,
            stats_port=description.stats_port,
        )

        self._session_host.connect("started", self.__on_host_started, description)
        self._session_host.connect("initializing", self.__on_session_initializing)
        self._session_host.connect("failed", self.__on_session_failed)
        self._session_host.create()

    def __on_host_started(self, session: SessionHost, description: Description) -> None:
        self._start_guest(description)

    def _start_guest(self, description: Description) -> None:
        self._session_guest = SessionGuest(
            data_path=description.data_path,
            address=description.address,
            session_port=description.session_port,
            messages_port=description.messages_port,
            scene_port=description.scene_port,
            stats_port=description.stats_port,
            widget=self._window,
        )

        self._session_guest.connect("started", self.__on_guest_started)
        self._session_guest.connect("initializing", self.__on_session_initializing)
        self._session_guest.connect("failed", self.__on_session_failed)
        self._session_guest.create()

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
        self._shutdown_guest()
        self._shutdown_host()
        Adw.Application.do_shutdown(self)

        logger.info("Client.Application.shut")


def main() -> None:
    application = Application()
    application.run(sys.argv)
