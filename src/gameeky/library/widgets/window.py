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

from typing import Optional, Any

from gi.repository import Gio, GLib, Gtk, GObject, Adw

from ...common.logger import logger
from ...common.config import pkgdatadir
from ...common.monitor import Monitor


@Gtk.Template(resource_path="/dev/tchx84/gameeky/library/widgets/window.ui")
class Window(Adw.ApplicationWindow):
    __gtype_name__ = "Window"

    __gsignals__ = {
        "changed": (GObject.SignalFlags.RUN_LAST, None, ()),
        "reload": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    source_buffer = Gtk.Template.Child()
    output_buffer = Gtk.Template.Child()
    execute_button = Gtk.Template.Child()
    stop_button = Gtk.Template.Child()
    banner = Gtk.Template.Child()

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self._process: Optional[Gio.Subprocess] = None
        self._cancellable = Gio.Cancellable()
        self._handler_id = self.source_buffer.connect(
            "changed", self.__on_source_changed
        )

        Monitor.default().connect("changed", self.__on_monitor_changed)

    @Gtk.Template.Callback("on_execute_clicked")
    def __on_execute_clicked(self, button: Gtk.Button) -> None:
        self.execute_button.props.visible = False
        self.stop_button.props.visible = True

        self._cancellable.reset()
        self.output_buffer.props.text = ""

        source, _ = Gio.File.new_tmp()
        source.replace_contents_async(
            contents=self.source_buffer.props.text.encode("UTF-8"),
            etag=None,
            make_backup=False,
            flags=Gio.FileCreateFlags.REPLACE_DESTINATION,
            cancellable=self._cancellable,
            callback=self.__on_written,
        )

    def __on_written(
        self,
        source: Gio.File,
        result: Gio.AsyncResult,
        data: Optional[Any] = None,
    ) -> None:
        try:
            source.replace_contents_finish(result)
        except Exception as e:
            logger.error(e)
            self._restore_ui()
            return

        launcher = Gio.SubprocessLauncher()
        launcher.setenv(
            variable="PYTHONPATH",
            value=pkgdatadir,
            overwrite=True,
        )
        launcher.set_flags(
            Gio.SubprocessFlags.STDOUT_PIPE | Gio.SubprocessFlags.STDERR_MERGE
        )

        self._process = launcher.spawnv(["python", source.get_path()])
        self._process.wait_async(
            cancellable=self._cancellable,
            callback=self.__on_finished,
            user_data=None,
        )

        self._queue_read(Gio.DataInputStream.new(self._process.get_stdout_pipe()))

    def __on_finished(
        self,
        process: Gio.Subprocess,
        result: Gio.AsyncResult,
        data: Optional[Any] = None,
    ) -> None:
        try:
            process.wait_finish(result)
        except Exception as e:
            logger.error(e)

        if not self._cancellable.is_cancelled():
            self._cancellable.cancel()

        self._process = None
        self._restore_ui()

    def _queue_read(self, stream: Gio.DataInputStream) -> None:
        stream.read_line_async(
            io_priority=GLib.PRIORITY_LOW,
            cancellable=self._cancellable,
            callback=self.__on_output,
            user_data=None,
        )

    def __on_output(
        self,
        stream: Gio.DataInputStream,
        result: Gio.AsyncResult,
        data: Optional[Any] = None,
    ) -> None:
        try:
            data, _ = stream.read_line_finish(result)
        except Exception as e:
            logger.error(e)
            self._restore_ui()
        else:
            self.output_buffer.insert_at_cursor(data.decode("UTF-8") + "\n")
            self._queue_read(stream)

    def _restore_ui(self) -> None:
        self.execute_button.props.visible = True
        self.stop_button.props.visible = False

    @Gtk.Template.Callback("on_stop_clicked")
    def __on_stop_clicked(self, button: Gtk.Button) -> None:
        if self._process is None:
            return

        self._cancellable.cancel()
        self._process.force_exit()

    def __on_source_changed(
        self,
        buffer: Gtk.TextBuffer,
        user_data: Optional[Any] = None,
    ) -> None:
        self.emit("changed")

    def __on_monitor_changed(self, monitor: Monitor) -> None:
        self.banner.props.revealed = True

    @Gtk.Template.Callback("on_reload_clicked")
    def __on_reload_clicked(
        self,
        banner: Adw.Banner,
        user_data: Optional[Any] = None,
    ) -> None:
        self.emit("reload")
        self.banner.props.revealed = False

    @property
    def source(self) -> str:
        return self.source_buffer.props.text

    @source.setter
    def source(self, text: str) -> None:
        self.source_buffer.handler_block(self._handler_id)
        self.source_buffer.props.text = text
        self.source_buffer.handler_unblock(self._handler_id)
