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

from gi.repository import Gtk, Adw

from ...common.scanner import Description


@Gtk.Template(resource_path="/dev/tchx84/gameeky/launcher/widgets/project_settings.ui")  # fmt: skip
class ProjectSettings(Adw.PreferencesGroup):
    __gtype_name__ = "ProjectSettings"

    _name = Gtk.Template.Child()
    _description = Gtk.Template.Child()

    @property
    def description(self) -> Description:
        return Description(
            name=self._name.props.text,
            description=self._description.props.text,
        )

    @description.setter
    def description(self, description: Description) -> None:
        self._name.props.text = description.name
        self._description.props.text = description.description
