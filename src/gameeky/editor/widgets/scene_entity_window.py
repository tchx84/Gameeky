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

from .entity_settings import EntitySettings

from ..models.scene import Scene as SceneModel, Entity


@Gtk.Template(resource_path="/dev/tchx84/gameeky/editor/widgets/scene_entity_window.ui")  # fmt: skip
class SceneEntityWindow(Adw.Window):
    __gtype_name__ = "SceneEntityWindow"

    content = Gtk.Template.Child()

    def __init__(self, entity: Entity, model: SceneModel, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self._entity = entity
        self._model = model

        self._entity_settings = EntitySettings()
        self._entity_settings.description = self._entity.description

        self.content.props.child = self._entity_settings

    @Gtk.Template.Callback("on_cancel_clicked")
    def __on_cancel_clicked(self, button: Gtk.Button) -> None:
        self.destroy()

    @Gtk.Template.Callback("on_save_clicked")
    def __on_save_clicked(self, button: Gtk.Button) -> None:
        self._entity.description = self._entity_settings.description
        self.destroy()
