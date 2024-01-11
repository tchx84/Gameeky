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
from ...common.definitions import MAX_TCP_BYTES, DEFAULT_TIMEOUT


class Client(GObject.GObject):
    __gtype_name__ = "TCPClient"

    __gsignals__ = {
        "received": (GObject.SignalFlags.RUN_LAST, None, (object,)),
        "failed": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    def __init__(self, address: str, port: int, context: GLib.MainContext) -> None:
        super().__init__()

        self._client = Gio.SocketClient.new()
        self._client.set_timeout(DEFAULT_TIMEOUT)
        self._connection = self._client.connect_to_host(address, port, None)

        self._input_stream = self._connection.get_input_stream()
        self._output_stream = self._connection.get_output_stream()

        self._input_source = self._input_stream.create_source(None)
        self._input_source.set_callback(self.__on_data_received_db)
        self._input_source.attach(context)

        self._shut = False

    def __on_data_received_db(self, data: Optional[Any] = None) -> None:
        if self.shut is True:
            return

        try:
            raw = self._input_stream.read_bytes(MAX_TCP_BYTES, None)
        except Exception as e:
            logger.error(e)
            self.emit("failed")
        else:
            self.emit("received", raw.get_data())

    def send(self, data: bytes) -> None:
        if self.shut is True:
            return

        self._output_stream.write(data)

    def shutdown(self) -> None:
        self._connection.close()
        self._shut = True

        logger.debug("Client.TCP.shut")

    @property
    def shut(self) -> bool:
        return self._shut
