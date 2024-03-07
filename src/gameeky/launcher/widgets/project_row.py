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

from gi.repository import Gtk, GObject

from .project_row_popover import ProjectRowPopover

from ...common.scanner import Description
from ...common.config import VERSION


@Gtk.Template(resource_path="/dev/tchx84/gameeky/launcher/widgets/project_row.ui")
class ProjectRow(Gtk.FlowBoxChild):
    __gtype_name__ = "ProjectRow"

    __gsignals__ = {
        "edited": (GObject.SignalFlags.RUN_LAST, None, ()),
        "copied": (GObject.SignalFlags.RUN_LAST, None, ()),
        "removed": (GObject.SignalFlags.RUN_LAST, None, ()),
        "exported": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    title = Gtk.Template.Child()
    subtitle = Gtk.Template.Child()
    options = Gtk.Template.Child()

    def __init__(self, path: str) -> None:
        super().__init__()
        self.path = path

        self._popover = ProjectRowPopover(self)
        self._popover.set_parent(self.options)

    @Gtk.Template.Callback("on_options_clicked")
    def __on_options_clicked(self, button: Gtk.Button) -> None:
        self._popover.popup()

    @property
    def description(self) -> Description:
        return Description(
            name=self.title.props.label,
            description=self.subtitle.props.label,
            version=VERSION,
        )

    @description.setter
    def description(self, description: Description) -> None:
        self.title.props.label = description.name
        self.subtitle.props.label = description.description
