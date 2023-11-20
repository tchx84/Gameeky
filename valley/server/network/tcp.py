from typing import Any, Optional

from gi.repository import Gio, GLib, GObject

from ...common.logger import logger
from ...common.definitions import MAX_TCP_BYTES


class Client(GObject.GObject):
    __gtype_name__ = "TCPServerClient"

    def __init__(self, server: "Server", connection: Gio.SocketConnection) -> None:
        super().__init__()

        self._acknowledged = False
        self._server = server
        self._connection = connection
        self._input_stream = connection.get_input_stream()
        self._output_stream = connection.get_output_stream()

    def __str__(self) -> str:
        return self._connection.get_remote_address().to_string()

    def send(self, data: bytes) -> None:
        if self._server.shut is True:
            return

        self._output_stream.write(data)

    def run(self) -> None:
        while self._server.shut is False and self._connection.is_connected():
            try:
                raw = self._input_stream.read_bytes(MAX_TCP_BYTES, None)
            except:
                break

            data = raw.get_data()
            if not data:
                break

            if self._acknowledged is False:
                self._server.emit("connected", self, data)
                self._acknowledged = True
            else:
                self._server.emit("received", self, data)

        self._server.emit("disconnected", self)


class Server(GObject.GObject):
    __gtype_name__ = "TCPServer"

    __gsignals__ = {
        "connected": (GObject.SignalFlags.RUN_LAST, None, (object, object)),
        "received": (GObject.SignalFlags.RUN_LAST, None, (object, object)),
        "disconnected": (GObject.SignalFlags.RUN_LAST, None, (object,)),
    }

    def __init__(self, port: int, clients: int, context: GLib.MainContext) -> None:
        super().__init__()

        self._service = Gio.ThreadedSocketService.new(clients)
        self._service.add_inet_port(port)
        self._service.connect("run", self.__on_session_started_cb)
        self._service.start()

        self._shut = False

    def __on_session_started_cb(
        self,
        service: Gio.ThreadedSocketService,
        connection: Gio.SocketConnection,
        data: Optional[Any] = None,
    ) -> None:
        client = Client(server=self, connection=connection)
        client.run()

    def emit(self, *args) -> None:
        GLib.idle_add(GObject.GObject.emit, self, *args)

    def shutdown(self) -> None:
        self._service.stop()
        self._service.close()
        self._shut = True

        logger.info("Server.TCP.shut")

    @property
    def shut(self) -> bool:
        return self._shut
