import os

__dir__ = os.path.dirname(os.path.abspath(__file__))

from gi.repository import Gtk, Adw, GObject

from .utils import get_position_in_model
from .animation_settings import AnimationSettings

from ...common.scanner import Description


@Gtk.Template(filename=os.path.join(__dir__, "animation_row.ui"))
class AnimationRow(Adw.PreferencesGroup):
    __gtype_name__ = "AnimationRow"

    __gsignals__ = {
        "removed": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    button = Gtk.Template.Child()
    state_combo = Gtk.Template.Child()
    direction_combo = Gtk.Template.Child()
    animation_box = Gtk.Template.Child()

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self._animation_settings = AnimationSettings()

        # XXX Move these to UI file somehow
        self._animation_settings.connect("changed", self.__on_changed)
        self.state_combo.connect("notify::selected-item", self.__on_changed)
        self.direction_combo.connect("notify::selected-item", self.__on_changed)

        self.animation_box.append(self._animation_settings)

        self._update_description()

    def _update_description(self) -> None:
        self.props.description = (
            "By default"
            if self.state == "default"
            else f"While {self.state} {self.direction}"
        )

    def __on_changed(self, *args) -> None:
        self._update_description()

    @Gtk.Template.Callback("on_clicked")
    def __on_removed(self, button: Gtk.Button) -> None:
        self.emit("removed")

    @property
    def state(self) -> str:
        return self.state_combo.props.selected_item.props.string

    @state.setter
    def state(self, state: str) -> None:
        self.state_combo.props.selected = get_position_in_model(
            self.state_combo.props.model, state
        )

    @property
    def direction(self) -> str:
        return self.direction_combo.props.selected_item.props.string

    @direction.setter
    def direction(self, direction: str) -> None:
        self.direction_combo.props.selected = get_position_in_model(
            self.direction_combo.props.model, direction
        )

    @property
    def description(self) -> Description:
        return self._animation_settings.description

    @description.setter
    def description(self, description: Description) -> None:
        self._animation_settings.description = description
