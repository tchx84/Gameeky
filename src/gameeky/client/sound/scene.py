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
from gi.repository import GLib

from .entity import EntityRegistry

from ..game.scene import Scene as SceneModel

from ...common.logger import logger
from ...common.utils import add_idle_source, remove_source_id


class Scene:
    def __init__(self) -> None:
        self._idle_source_id: Optional[int] = None
        self._updated_source_id: Optional[int] = None
        self._model: Optional[SceneModel] = None

    def __on_model_updated(self, model: SceneModel) -> None:
        if self._idle_source_id is None:
            self._idle_source_id = add_idle_source(self._play)

    def _play(self, *args) -> int:
        if self._model is not None:
            for entity in self._model.entities:
                EntityRegistry.play(entity)

        if self._idle_source_id is not None:
            remove_source_id(self._idle_source_id)

        self._idle_source_id = None

        return GLib.SOURCE_REMOVE

    def _reset(self) -> None:
        if self._model is None:
            return

        if self._idle_source_id is not None:
            remove_source_id(self._idle_source_id)

        if self._updated_source_id is not None:
            self._model.disconnect(self._updated_source_id)

        self._model = None
        self._idle_source_id = None
        self._updated_source_id = None

    def shutdown(self) -> None:
        self._reset()

        logger.debug("Client.Sound.shut")

    @property
    def model(self) -> Optional[SceneModel]:
        return self._model

    @model.setter
    def model(self, model: Optional[SceneModel]) -> None:
        self._reset()

        self._model = model

        if self._model is None:
            return

        self._updated_source_id = self._model.connect(
            "ticked",
            self.__on_model_updated,
        )
