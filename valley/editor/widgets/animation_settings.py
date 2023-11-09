import os

__dir__ = os.path.dirname(os.path.abspath(__file__))

from typing import Optional

from gi.repository import Gtk, Gio, Adw, GObject, GLib

from .tile import Tile
from .animation import Animation

from ...common.logger import logger
from ...common.scanner import Description
from ...common.definitions import DEFAULT_TIMEOUT


@Gtk.Template(filename=os.path.join(__dir__, "animation_settings.ui"))
class AnimationSettings(Adw.PreferencesGroup):
    __gtype_name__ = "AnimationSettings"

    __gsignals__ = {
        "changed": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    tile_box = Gtk.Template.Child()
    animation_box = Gtk.Template.Child()
    path = Gtk.Template.Child()
    path_button = Gtk.Template.Child()
    columns = Gtk.Template.Child()
    rows = Gtk.Template.Child()
    duration = Gtk.Template.Child()
    scale_x = Gtk.Template.Child()
    scale_y = Gtk.Template.Child()
    crop_x = Gtk.Template.Child()
    crop_y = Gtk.Template.Child()
    flip_x = Gtk.Template.Child()
    flip_y = Gtk.Template.Child()
    first_frame = Gtk.Template.Child()
    last_frame = Gtk.Template.Child()

    def __init__(self) -> None:
        super().__init__()
        self._handler_id: Optional[int] = None

        self._tile = Tile()
        self._animation = Animation()

        self.tile_box.append(self._tile)
        self.animation_box.append(self._animation)

    @Gtk.Template.Callback("on_path_button_clicked")
    def __on_path_button_clicked(self, button: Gtk.Button) -> None:
        dialog = Gtk.FileDialog()
        dialog.open(callback=self.__on_open_dialog_finish)

    def __on_open_dialog_finish(
        self,
        dialog: Gtk.FileDialog,
        result: Gio.AsyncResult,
    ) -> None:
        try:
            file = dialog.open_finish(result)
        except Exception as e:
            logger.error(e)
        else:
            self.path.props.text = file.get_path()

    @Gtk.Template.Callback("on_animation_changed")
    def __on_animation_changed(self, *args) -> None:
        if self._handler_id is not None:
            GLib.Source.remove(self._handler_id)

        self._handler_id = GLib.timeout_add_seconds(
            DEFAULT_TIMEOUT / 2,
            self.__on_animation_change_delayed,
        )

    def __on_animation_change_delayed(self) -> int:
        self._tile.update(self.description)
        self._animation.update(self.description)

        self.emit("changed")
        self._handler_id = None
        return GLib.SOURCE_REMOVE

    @property
    def description(self) -> Description:
        return Description(
            path=self.path.props.text,
            columns=int(self.columns.props.value),
            rows=int(self.rows.props.value),
            duration=round(self.duration.props.value, 1),
            scale_x=round(self.scale_x.props.value, 1),
            scale_y=round(self.scale_y.props.value, 1),
            crop_x=int(self.crop_x.props.value),
            crop_y=int(self.crop_y.props.value),
            flip_x=self.flip_x.props.active,
            flip_y=self.flip_y.props.active,
            first_frame=int(self.first_frame.props.value),
            last_frame=int(self.last_frame.props.value),
        )

    @description.setter
    def description(self, description: Description) -> None:
        self.path.props.text = description.path
        self.columns.props.value = description.columns
        self.rows.props.value = description.rows
        self.duration.props.value = description.duration
        self.scale_x.props.value = description.scale_x
        self.scale_y.props.value = description.scale_y
        self.crop_x.props.value = description.crop_x
        self.crop_y.props.value = description.crop_y
        self.flip_x.props.active = description.flip_x
        self.flip_y.props.active = description.flip_y
        self.first_frame.props.value = description.first_frame
        self.last_frame.props.value = description.last_frame
