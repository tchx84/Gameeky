from gi.repository import Gtk, Adw, GObject

from .utils import get_position_in_model
from .sound_settings import SoundSettings

from ...common.scanner import Description


@Gtk.Template(resource_path="/dev/tchx84/gameeky/editor/widgets/sound_row.ui")
class SoundRow(Adw.PreferencesGroup):
    __gtype_name__ = "SoundRow"

    __gsignals__ = {
        "cloned": (GObject.SignalFlags.RUN_LAST, None, ()),
        "removed": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    state_combo = Gtk.Template.Child()
    sound_box = Gtk.Template.Child()

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self._sound_settings = SoundSettings()

        # XXX Move these to UI file somehow
        self._sound_settings.connect("changed", self.__on_changed)
        self.state_combo.connect("notify::selected-item", self.__on_changed)

        self.sound_box.append(self._sound_settings)

        self._update_description()

    def _update_description(self) -> None:
        self.props.description = f"While {self.state}"

    def __on_changed(self, *args) -> None:
        self._update_description()

    @Gtk.Template.Callback("on_remove_clicked")
    def __on_remove_clicked(self, button: Gtk.Button) -> None:
        self.emit("removed")

    @Gtk.Template.Callback("on_clone_clicked")
    def __on_clone_clicked(self, button: Gtk.Button) -> None:
        self.emit("cloned")

    @property
    def state(self) -> str:
        return self.state_combo.props.selected_item.props.string

    @state.setter
    def state(self, state: str) -> None:
        self.state_combo.props.selected = get_position_in_model(
            self.state_combo.props.model, state
        )

    @property
    def description(self) -> Description:
        return self._sound_settings.description

    @description.setter
    def description(self, description: Description) -> None:
        self._sound_settings.description = description

    def shutdown(self) -> None:
        self._sound_settings.shutdown()
