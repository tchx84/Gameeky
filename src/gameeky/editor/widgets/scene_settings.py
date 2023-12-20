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

from typing import List
from gi.repository import Gio, Gtk, Adw

from .dropdown_helper import DropDownHelper

from ..models.entity import Entity
from ..models.daytime_row import DayTimeRow as DayTimeRowModel

from ...common.logger import logger
from ...common.utils import get_project_path, get_project_folder, clamp
from ...common.scanner import Description
from ...common.vector import Vector


@Gtk.Template(resource_path="/dev/tchx84/gameeky/editor/widgets/scene_settings.ui")  # fmt: skip
class SceneSettings(Adw.PreferencesGroup):
    __gtype_name__ = "SceneSettings"

    name = Gtk.Template.Child()
    project = Gtk.Template.Child()
    daytime = Gtk.Template.Child()
    width = Gtk.Template.Child()
    height = Gtk.Template.Child()

    def __init__(self) -> None:
        super().__init__()
        self._spawn = Vector(0, 0, 0)
        self._entities: List[Entity] = []
        self.project.props.text = get_project_path("")

        self._daytime = DropDownHelper(self.daytime, DayTimeRowModel)

    @Gtk.Template.Callback("on_open_clicked")
    def __on_open_clicked(self, button: Gtk.Button) -> None:
        folder = get_project_folder("")

        dialog = Gtk.FileDialog()
        dialog.props.initial_folder = folder
        dialog.select_folder(callback=self.__on_open_dialog_finish)

    def __on_open_dialog_finish(
        self,
        dialog: Gtk.FileDialog,
        result: Gio.AsyncResult,
    ) -> None:
        try:
            file = dialog.select_folder_finish(result)
        except Exception as e:
            logger.error(e)
        else:
            self.project.props.text = file.get_path()

    @property
    def title(self) -> str:
        return self.name.props.text

    @property
    def project_path(self) -> None:
        return self.project.props.text

    @property
    def description(self) -> Description:
        width = int(self.width.props.value)
        height = int(self.height.props.value)

        # Remove entities that are no longer contained within the new dimensions

        for entity in list(self._entities):
            if entity.position.x >= width or entity.position.y >= height:
                self._entities.remove(entity)

        # Make sure spawn point is within the new dimensions

        self._spawn.x = clamp(width - 1, 0, self._spawn.x)
        self._spawn.y = clamp(height - 1, 0, self._spawn.y)

        return Description(
            name=self.name.props.text,
            width=width,
            height=height,
            spawn=self._spawn,
            daytime=self._daytime.value,
            entities=self._entities,
        )

    @description.setter
    def description(self, description: Description) -> None:
        self.name.props.text = description.name
        self.width.props.value = description.width
        self.height.props.value = description.height
        self._daytime.value = description.daytime

        self._spawn = description.spawn
        self._entities = description.entities
