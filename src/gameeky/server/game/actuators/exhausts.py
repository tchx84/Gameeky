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

from ..definitions import Cost

from ....common.definitions import Action


class Actuator(BaseActuator):
    __stamina_cost_by_action__ = {
        Action.MOVE: Cost.MAX,
        Action.USE: Cost.MAX * 4,
        Action.TAKE: Cost.MAX * 4,
    }

    name = "exhausts"
    interactable = False
    activatable = True

    def tick(self) -> None:
        seconds = self._seconds_since_activation()

        cost = self.__stamina_cost_by_action__.get(self._entity.action, Cost.MIN)
        gain = abs(cost) * self._entity.recovery
        self._entity.stamina += (gain - (cost - Cost.MIN)) * seconds

        if self._entity.stamina <= 0 or self.activated is True:
            self._entity.perform(Action.EXHAUST)

        super().tick()
