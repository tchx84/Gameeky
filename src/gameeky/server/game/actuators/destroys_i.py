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

from __future__ import annotations

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..entity import Entity

from .base import Actuator as BaseActuator

from ....common.definitions import Action


class Actuator(BaseActuator):
    name = "destroys_i"
    interactable = True
    activatable = True

    def prepare(self, interactee: Optional[Entity] = None) -> bool:
        if interactee is None:
            return False

        if not self._entity.targets(interactee):
            return False

        return super().prepare(interactee)

    def tick(self) -> None:
        if self._interactee is None and self.activated is False:
            return

        self._entity.stop()
        self._entity.perform(Action.DESTROY)

        super().tick()
