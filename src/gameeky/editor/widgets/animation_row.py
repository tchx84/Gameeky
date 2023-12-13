from gettext import gettext as _
from gi.repository import Gtk, Adw, GObject

from .animation_settings import AnimationSettings
from .dropdown_helper import DropDownHelper

from ..models.direction_row import DirectionRow as DirectionRowModel
from ..models.state_row import StateRow as StateRowModel

from ...common.scanner import Description


@Gtk.Template(resource_path="/dev/tchx84/gameeky/editor/widgets/animation_row.ui")
class AnimationRow(Adw.PreferencesGroup):
    __gtype_name__ = "AnimationRow"

    __gsignals__ = {
        "cloned": (GObject.SignalFlags.RUN_LAST, None, ()),
        "removed": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    state_combo = Gtk.Template.Child()
    direction_combo = Gtk.Template.Child()
    animation_box = Gtk.Template.Child()

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)

        # XXX Move these to UI file somehow
        self._animation_settings = AnimationSettings()
        self._animation_settings.connect("changed", self.__on_changed)
        self.animation_box.append(self._animation_settings)

        self._state = DropDownHelper(self.state_combo, StateRowModel, True)
        self._state.connect("changed", self.__on_changed)

        self._direction = DropDownHelper(self.direction_combo, DirectionRowModel, True)
        self._direction.connect("changed", self.__on_changed)

        self._update_description()

    def _update_description(self) -> None:
        description = _("While %s") % self._state.text.lower()

        if self.direction != "default":
            description += f" {self._direction.text.lower()}"
        if self.state == "default":
            description = _("By default")

        self.props.description = description

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
    def direction(self) -> str:
        return self._direction.value

    @direction.setter
    def direction(self, value: str) -> None:
        self._direction.value = value

    @property
    def description(self) -> Description:
        return self._animation_settings.description

    @description.setter
    def description(self, description: Description) -> None:
        self._animation_settings.description = description

    def shutdown(self) -> None:
        self._animation_settings.shutdown()
