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

from typing import Callable, List, Tuple, Optional

from gi.repository import GObject


class ChangeSignalHelper(GObject.GObject):
    __signal__ = "changed"

    def __init__(self, callback: Callable) -> None:
        self._callback = callback
        self._handlers: List[Tuple[GObject.GObject, int]] = []

    def add(self, obj: GObject.GObject, signal: Optional[str] = None) -> None:
        signal = self.__signal__ if signal is None else signal

        handler = obj.connect(signal, self._callback)

        self._handlers.append((obj, handler))

    def block(self) -> None:
        for obj, handler in self._handlers:
            obj.handler_block(handler)

    def unblock(self) -> None:
        for obj, handler in self._handlers:
            obj.handler_unblock(handler)

    def shutdown(self) -> None:
        for obj, handler in self._handlers:
            obj.disconnect(handler)
