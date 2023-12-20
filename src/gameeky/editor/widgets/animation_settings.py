# Copyright (c) 2023 Martín Abente Lahaye.
#
# This file is part of Gameeky
# (see gameeky.tchx84.dev).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from typing import Optional

from gi.repository import Gtk, Gio, Adw, GObject, GLib

from .animation import Animation
from .tileset_window import TilesetWindow

from ...common.logger import logger
from ...common.utils import get_project_folder, get_relative_path
from ...common.scanner import Description
from ...common.definitions import DEFAULT_TIMEOUT


@Gtk.Template(resource_path="/dev/tchx84/gameeky/editor/widgets/animation_settings.ui")  # fmt: skip
class AnimationSettings(Adw.PreferencesGroup):
    __gtype_name__ = "AnimationSettings"

    __gsignals__ = {
        "changed": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

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
    rotate = Gtk.Template.Child()
    tiles_x = Gtk.Template.Child()
    tiles_y = Gtk.Template.Child()

    def __init__(self) -> None:
        super().__init__()
        self._handler_id: Optional[int] = None
        self._tileset: Optional[TilesetWindow] = None

        self._animation = Animation()
        self.animation_box.append(self._animation)

        # XXX Move the UI file somehow
        self.flip_x.connect("notify::active", self.__on_animation_changed)
        self.flip_y.connect("notify::active", self.__on_animation_changed)

    def _update_tileset(self) -> None:
        if self._tileset is None:
            return

        description = self.description

        self._tileset.rows = description.rows
        self._tileset.columns = description.columns
        self._tileset.path = description.path

    def __on_close_tileset(self, tileset: TilesetWindow) -> None:
        if self._tileset is None:
            return

        self._tileset.disconnect_by_func(self.__on_close_tileset)
        self._tileset.destroy()
        self._tileset = None

    @Gtk.Template.Callback("on_view_button_clicked")
    def __on_view_button_clicked(self, button: Gtk.Button) -> None:
        self._tileset = TilesetWindow()
        self._tileset.connect("close-request", self.__on_close_tileset)
        self._tileset.present()

        self._update_tileset()

    @Gtk.Template.Callback("on_path_button_clicked")
    def __on_path_button_clicked(self, button: Gtk.Button) -> None:
        folder = get_project_folder("assets")

        png_filter = Gtk.FileFilter()
        png_filter.add_pattern("*.png")

        dialog = Gtk.FileDialog()
        dialog.props.initial_folder = folder
        dialog.props.default_filter = png_filter
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
        self._animation.update(self.description)
        self._update_tileset()

        self.emit("changed")
        self._handler_id = None
        return GLib.SOURCE_REMOVE

    @property
    def description(self) -> Description:
        return Description(
            path=get_relative_path(self.path.props.text),
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
            rotate=float(self.rotate.props.value),
            tiles_x=int(self.tiles_x.props.value),
            tiles_y=int(self.tiles_y.props.value),
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
        self.rotate.props.value = description.rotate
        self.tiles_x.props.value = description.tiles_x
        self.tiles_y.props.value = description.tiles_y

    def shutdown(self) -> None:
        self._animation.shutdown()
