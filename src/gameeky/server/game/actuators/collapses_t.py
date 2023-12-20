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

from .base import Actuator as BaseActuator

from ....common.definitions import Action
from ....common.utils import get_time_milliseconds


class Actuator(BaseActuator):
    name = "collapses_t"
    interactable = False
    activatable = False

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self._timestamp = get_time_milliseconds()

    def tick(self) -> None:
        if (get_time_milliseconds() - self._timestamp) / 1000 <= self._entity.rate:
            return

        self._entity.stop()
        self._entity.perform(Action.DESTROY)
