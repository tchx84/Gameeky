import os

__dir__ = os.path.dirname(os.path.abspath(__file__))

from gi.repository import Gtk, Adw, GObject

from ...common.utils import get_data_path
from ...common.definitions import (
    DEFAULT_SCENE,
    DEFAULT_CLIENTS,
    DEFAULT_ADDRESS,
    DEFAULT_SESSION_PORT,
    DEFAULT_MESSAGES_PORT,
    DEFAULT_SCENE_PORT,
    DEFAULT_STATS_PORT,
)


@Gtk.Template(filename=os.path.join(__dir__, "session.ui"))
class Session(Adw.PreferencesWindow):
    __gtype_name__ = "Session"

    __gsignals__ = {
        "done": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    scene_group = Gtk.Template.Child()
    data_dir_entry = Gtk.Template.Child()
    scene_entry = Gtk.Template.Child()
    clients_spin = Gtk.Template.Child()
    address_entry = Gtk.Template.Child()
    session_port_entry = Gtk.Template.Child()
    messages_port_entry = Gtk.Template.Child()
    scene_port_entry = Gtk.Template.Child()
    stats_port_entry = Gtk.Template.Child()
    create_button = Gtk.Template.Child()

    def __init__(self, host: bool, *args, **kargs) -> None:
        super().__init__(*args, **kargs)

        self._host = host
        self.scene_group.props.visible = self._host

        self.data_dir_entry.props.text = get_data_path("")
        self.scene_entry.props.text = DEFAULT_SCENE
        self.clients_spin.props.value = DEFAULT_CLIENTS
        self.address_entry.props.text = DEFAULT_ADDRESS
        self.session_port_entry.props.text = str(DEFAULT_SESSION_PORT)
        self.messages_port_entry.props.text = str(DEFAULT_MESSAGES_PORT)
        self.scene_port_entry.props.text = str(DEFAULT_SCENE_PORT)
        self.stats_port_entry.props.text = str(DEFAULT_STATS_PORT)

        self.create_button.connect("clicked", self.__on_button_clicked)

    def __on_button_clicked(self, button: Gtk.Button) -> None:
        self.emit("done")
        self.close()

    @property
    def data_dir(self) -> str:
        return self.data_dir_entry.props.text

    @property
    def scene(self) -> str:
        return self.scene_entry.props.text

    @property
    def clients(self) -> int:
        return self.clients_spin.props.value

    @property
    def address(self) -> str:
        return self.address_entry.props.text

    @property
    def session_port(self) -> int:
        return int(self.session_port_entry.props.text)

    @property
    def messages_port(self) -> int:
        return int(self.messages_port_entry.props.text)

    @property
    def scene_port(self) -> int:
        return int(self.scene_port_entry.props.text)

    @property
    def stats_port(self) -> int:
        return int(self.stats_port_entry.props.text)

    @property
    def host(self) -> bool:
        return self._host
