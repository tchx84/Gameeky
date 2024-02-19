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

from typing import Any, Optional

from gi.repository import GLib, Gio, GObject

from ...common.logger import logger
from ...common.definitions import DEFAULT_SEPARATOR


class Client(GObject.GObject):
    __gtype_name__ = "TCPClient"

    __gsignals__ = {
        "received": (GObject.SignalFlags.RUN_LAST, None, (str,)),
        "failed": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    def __init__(
        self,
        address: str,
        port: int,
        context: GLib.MainContext,
        graceful: bool,
    ) -> None:
        super().__init__()

        self._client = Gio.SocketClient.new()
        self._connection = self._client.connect_to_host(address, port, None)
        self._connection.set_graceful_disconnect(graceful)

        self._cancellable = Gio.Cancellable()
        self._data_input_stream = Gio.DataInputStream.new(
            self._connection.get_input_stream()
        )
        self._data_output_stream = Gio.DataOutputStream.new(
            self._connection.get_output_stream()
        )

        self._listen()

    def __on_line_read(
        self,
        stream: Gio.DataInputStream,
        result: Gio.AsyncResult,
        data: Optional[Any] = None,
    ) -> None:
        try:
            data, _ = stream.read_line_finish(result)
        except Exception as e:
            logger.error(e)
            self.emit("failed")
            return

        if not data:
            return

        self.emit("received", data.decode("UTF-8"))
        self._listen()

    def _listen(self) -> None:
        self._data_input_stream.read_line_async(
            GLib.PRIORITY_DEFAULT,
            self._cancellable,
            self.__on_line_read,
            None,
        )

    def send(self, data: str) -> None:
        if self._cancellable.is_cancelled() is True:
            return

        self._data_output_stream.put_string(data + DEFAULT_SEPARATOR)

    def shutdown(self) -> None:
        self._cancellable.cancel()
        self._connection.close()

        logger.debug("Client.TCP.shut")
