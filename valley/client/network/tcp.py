from gi.repository import Gio, GObject


class Client(GObject.GObject):
    __gtype_name__ = "TCPClient"

    __gsignals__ = {
        "received": (GObject.SignalFlags.RUN_LAST, None, (object,)),
    }

    MAX_BYTES = 2048

    def __init__(self, address, port, context):
        super().__init__()

        self._client = Gio.SocketClient.new()
        self._connection = self._client.connect_to_host(address, port, None)

        self._input_stream = self._connection.get_input_stream()
        self._output_stream = self._connection.get_output_stream()

        self._input_source = self._input_stream.create_source(None)
        self._input_source.set_callback(self.__on_data_received_db)
        self._input_source.attach(context)

    def __on_data_received_db(self, source):
        raw = self._input_stream.read_bytes(self.MAX_BYTES, None)
        self.emit("received", raw.get_data())

    def send(self, data):
        self._output_stream.write(data)
