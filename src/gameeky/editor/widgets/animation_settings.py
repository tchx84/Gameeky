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

from gi.repository import Gtk, Gio, GLib, Adw, GObject

from .animation import Animation
from .tileset_window import TilesetWindow
from .change_signal_helper import ChangeSignalHelper

from ...common.logger import logger
from ...common.utils import get_project_folder, get_relative_path
from ...common.scanner import Description


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
        self._tileset: Optional[TilesetWindow] = None

        self._animation = Animation()
        self.animation_box.append(self._animation)

        self._changes = ChangeSignalHelper(self.__on_changed)
        self._changes.add(self.path)
        self._changes.add(self.columns)
        self._changes.add(self.rows)
        self._changes.add(self.first_frame)
        self._changes.add(self.last_frame)
        self._changes.add(self.duration)
        self._changes.add(self.rotate)
        self._changes.add(self.tiles_x)
        self._changes.add(self.tiles_y)
        self._changes.add(self.scale_x)
        self._changes.add(self.scale_y)
        self._changes.add(self.crop_x)
        self._changes.add(self.crop_y)
        self._changes.add(self.flip_x, signal="notify::active")
        self._changes.add(self.flip_y, signal="notify::active")

    def _update(self) -> None:
        description = self.description

        self._animation.update(description)
        self._update_tileset(description)

    def _update_tileset(self, description: Description) -> None:
        if self._tileset is None:
            return

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

        self._update_tileset(self.description)

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

    def __on_changed(self, *args) -> None:
        self._update()
        self.emit("changed")

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
        self._changes.block()

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

        GLib.idle_add(self._update)

        self._changes.unblock()

    def shutdown(self) -> None:
        self._animation.shutdown()
