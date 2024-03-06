# Copyright (c) 2024 Martín Abente Lahaye.
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

from __future__ import annotations

import os

from typing import TYPE_CHECKING

from gi.repository import GLib, Gtk

if TYPE_CHECKING:
    from .project_row import ProjectRow

from ...common.utils import launch_player, launch_scene, valid_file
from ...common.definitions import DEFAULT_SCENE


@Gtk.Template(resource_path="/dev/tchx84/gameeky/launcher/widgets/project_row_popover.ui")  # fmt: skip
class ProjectRowPopover(Gtk.Popover):
    __gtype_name__ = "ProjectRowPopover"

    play = Gtk.Template.Child()
    edit = Gtk.Template.Child()
    settings = Gtk.Template.Child()
    copy = Gtk.Template.Child()
    delete = Gtk.Template.Child()

    def __init__(self, row: ProjectRow) -> None:
        super().__init__()
        self.row = row
        writeable = GLib.access(self.row.path, os.W_OK) == 0

        self.edit.props.sensitive = writeable
        self.settings.props.sensitive = writeable
        self.delete.props.sensitive = writeable

    def popup(self) -> None:
        self.play.props.sensitive = valid_file(self.default_scene)
        super().popup()

    @Gtk.Template.Callback("on_activated")
    def __on_activated(self, box: Gtk.ListBox, row: Gtk.ListBoxRow) -> None:
        if row == self.play:
            launch_player(self.row.path, self.default_scene)
        elif row == self.edit:
            launch_scene(self.row.path, self.default_scene)
        elif row == self.settings:
            self.row.emit("edited")
        elif row == self.copy:
            self.row.emit("copied")
        elif row == self.delete:
            self.row.emit("removed")

        self.popdown()

    @property
    def default_scene(self) -> str:
        return os.path.join(self.row.path, DEFAULT_SCENE)
