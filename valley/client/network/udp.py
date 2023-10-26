from typing import Any, Optional

from gi.repository import Gio, GLib, GObject

from ...common.logger import logger
from ...common.definitions import MAX_UDP_BYTES


class Client(GObject.GObject):
    __gtype_name__ = "UDPClient"

    __gsignals__ = {
        "received": (GObject.SignalFlags.RUN_LAST, None, (object, object)),
    }

    def __init__(self, address: str, port: int, context: GLib.MainContext) -> None:
        super().__init__()

        self._address = Gio.InetSocketAddress.new_from_string(address, port)

        self._socket = Gio.Socket.new(
            Gio.SocketFamily.IPV4, Gio.SocketType.DATAGRAM, Gio.SocketProtocol.UDP
        )
        self._socket.connect(self._address)

        self._input_stream = Gio.UnixInputStream.new(self._socket.get_fd(), False)

        self._source = self._socket.create_source(GLib.IOCondition.IN, None)
        self._source.set_callback(self.__received_data_cb)
        self._source.attach(context)

    def __received_data_cb(self, data: Optional[Any] = None) -> int:
        # XXX replace with .receive_from() when fixed
        size, address, messages, flags = self._socket.receive_message(
            [], Gio.SocketMsgFlags.PEEK, None
        )
        raw = self._input_stream.read_bytes(MAX_UDP_BYTES, None)

        self.emit("received", address, raw.get_data())

        return GLib.SOURCE_CONTINUE

    def send(self, data: bytes) -> None:
        # XXX raise specific errors to allow clients to gracefully handle it
        try:
            self._socket.send(data)
        except Exception as e:
            logger.error(e)
