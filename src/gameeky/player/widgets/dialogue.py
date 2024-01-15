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

from typing import Optional

from gi.repository import Gtk

from ...client.game.dialogue import Dialogue as DialogueModel


@Gtk.Template(resource_path="/dev/tchx84/gameeky/player/widgets/dialogue.ui")
class Dialogue(Gtk.Box):
    __gtype_name__ = "Dialogue"

    label = Gtk.Template.Child()

    def __init__(self) -> None:
        super().__init__()
        self._model: Optional[DialogueModel] = None
        self._updated_source_id: Optional[int] = None

    def __on_updated(self, model: DialogueModel) -> None:
        self.label.props.label = model.text
        self.props.visible = True

    @Gtk.Template.Callback("on_clicked")
    def __on_activated(self, button: Gtk.Button) -> None:
        self.props.visible = False

    @property
    def model(self) -> Optional[DialogueModel]:
        return self._model

    @model.setter
    def model(self, model: DialogueModel) -> None:
        if self._model is not None and self._updated_source_id is not None:
            self._model.disconnect(self._updated_source_id)

        if model is not None:
            self._updated_source_id = model.connect("updated", self.__on_updated)

        self._model = model
