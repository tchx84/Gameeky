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

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..entity import Entity

from ....common.utils import get_time_milliseconds


class Handler:
    def __init__(self, entity: Entity) -> None:
        self.busy = False

        self._entity = entity

        timestamp = get_time_milliseconds()
        self._timestamp_prepare = timestamp
        self._timestamp_tick = timestamp
        self._timestamp_finish = timestamp

    def _get_elapsed_seconds_since_tick(self) -> float:
        return (get_time_milliseconds() - self._timestamp_tick) / 1000

    def _get_elapsed_seconds_since_prepare(self) -> float:
        return (get_time_milliseconds() - self._timestamp_prepare) / 1000

    def _get_elapsed_seconds_since_finish(self) -> float:
        return (get_time_milliseconds() - self._timestamp_finish) / 1000

    def prepare(self, value: float) -> bool:
        self.busy = True
        self._timestamp_prepare = get_time_milliseconds()
        self._timestamp_tick = get_time_milliseconds()

        return True

    def tick(self) -> None:
        self._timestamp_tick = get_time_milliseconds()

    def finish(self) -> None:
        self.busy = False
        self._timestamp_finish = get_time_milliseconds()

    def cancel(self) -> None:
        self.finish()
