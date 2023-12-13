from gettext import gettext as _
from gi.repository import Gtk, Adw, GObject

from .sound_settings import SoundSettings
from .dropdown_helper import DropDownHelper

from ..models.state_row import StateRow as StateRowModel

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

        # XXX Move these to UI file somehow
        self._sound_settings = SoundSettings()
        self._sound_settings.connect("changed", self.__on_changed)
        self.sound_box.append(self._sound_settings)

        self._state = DropDownHelper(self.state_combo, StateRowModel)
        self._state.connect("changed", self.__on_changed)

        self._update_description()

    def _update_description(self) -> None:
        self.props.description = _(f"While {self._state.text.lower()}")

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
        return self._state.value

    @state.setter
    def state(self, value: str) -> None:
        self._state.value = value

    @property
    def description(self) -> Description:
        return self._sound_settings.description

    @description.setter
    def description(self, description: Description) -> None:
        self._sound_settings.description = description

    def shutdown(self) -> None:
        self._sound_settings.shutdown()
