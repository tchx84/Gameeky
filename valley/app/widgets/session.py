import os

__dir__ = os.path.dirname(os.path.abspath(__file__))

from gi.repository import Gtk, Adw, GObject


@Gtk.Template(filename=os.path.join(__dir__, "session.ui"))
class Session(Adw.PreferencesWindow):
    __gtype_name__ = "Session"

    __gsignals__ = {
        "done": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    _data_dir = Gtk.Template.Child()
    _scene = Gtk.Template.Child()
    _clients = Gtk.Template.Child()
    _session_port = Gtk.Template.Child()
    _messages_port = Gtk.Template.Child()
    _scene_port = Gtk.Template.Child()
    _stats_port = Gtk.Template.Child()
    _create = Gtk.Template.Child()

    def __init__(
        self,
        data_dir: str,
        scene: str,
        clients: int,
        session_port: int,
        messages_port: int,
        scene_port: int,
        stats_port: int,
        *args,
        **kargs,
    ) -> None:
        super().__init__(*args, **kargs)

        self._data_dir.props.text = data_dir
        self._scene.props.text = scene
        self._clients.props.value = clients
        self._session_port.props.text = str(session_port)
        self._messages_port.props.text = str(messages_port)
        self._scene_port.props.text = str(scene_port)
        self._stats_port.props.text = str(stats_port)

        self._create.connect("clicked", self.__on_button_clicked)

    def __on_button_clicked(self, button: Gtk.Button) -> None:
        self.emit("done")
        self.close()

    @property
    def data_dir(self) -> str:
        return self._data_dir.props.text

    @property
    def scene(self) -> str:
        return self._scene.props.text

    @property
    def clients(self) -> int:
        return self._clients.props.value

    @property
    def session_port(self) -> int:
        return int(self._session_port.props.text)

    @property
    def messages_port(self) -> int:
        return int(self._messages_port.props.text)

    @property
    def scene_port(self) -> int:
        return int(self._scene_port.props.text)

    @property
    def stats_port(self) -> int:
        return int(self._stats_port.props.text)
