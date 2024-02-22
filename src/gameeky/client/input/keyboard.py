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

from typing import Dict, Optional, Tuple

from gi.repository import Gdk, Gtk, GLib

from ..game.service import Service

from ...common.logger import logger
from ...common.utils import add_idle_source
from ...common.session import Session
from ...common.definitions import Action, Direction


class Keyboard(Gtk.EventControllerKey):
    action_by_combo = {
        (Gdk.KEY_Right, 0): (Action.MOVE, Direction.EAST),
        (Gdk.KEY_Up, 0): (Action.MOVE, Direction.NORTH),
        (Gdk.KEY_Left, 0): (Action.MOVE, Direction.WEST),
        (Gdk.KEY_Down, 0): (Action.MOVE, Direction.SOUTH),
        (Gdk.KEY_u, 0): (Action.USE, 0),
        (Gdk.KEY_t, 0): (Action.TAKE, 0),
        (Gdk.KEY_d, 0): (Action.DROP, 0),
        (Gdk.KEY_i, 0): (Action.INTERACT, 0),
        (Gdk.KEY_Right, Gdk.ModifierType.CONTROL_MASK): (Action.ROTATE, Direction.EAST),
        (Gdk.KEY_Up, Gdk.ModifierType.CONTROL_MASK): (Action.ROTATE, Direction.NORTH),
        (Gdk.KEY_Left, Gdk.ModifierType.CONTROL_MASK): (Action.ROTATE, Direction.WEST),
        (Gdk.KEY_Down, Gdk.ModifierType.CONTROL_MASK): (Action.ROTATE, Direction.SOUTH),
    }

    def __init__(
        self,
        widget: Gtk.Widget,
        service: Service,
        context: GLib.MainContext,
    ) -> None:
        super().__init__()
        self._is_pressed_by_combo: Dict[Tuple[int, int], bool] = {}
        self._registered_source_id: Optional[int] = None
        self._key_pressed_source_id: Optional[int] = None
        self._key_released_source_id: Optional[int] = None

        self._widget = widget
        self._widget.add_controller(self)

        self._service = service
        self._registered_source_id = self._service.connect(
            "registered",
            self.__on_service_registered,
        )

        self._context = context

    def __on_service_registered(self, service: Service, session: Session) -> None:
        self._key_pressed_source_id = self.connect(
            "key-pressed",
            self.__on_key_pressed,
        )
        self._key_released_source_id = self.connect(
            "key-released",
            self.__on_key_released,
        )

    def __on_key_pressed(
        self,
        controller: Gtk.EventControllerKey,
        key: int,
        code: int,
        state: Gdk.ModifierType,
    ) -> None:
        combo = (key, state)

        if self._is_pressed_by_combo.get(combo) is True:
            return

        action, value = self.action_by_combo.get(combo, (None, 0))
        if action is None:
            return

        self._is_pressed_by_combo[combo] = True
        self._message(action, value)

    def __on_key_released(
        self,
        controller: Gtk.EventControllerKey,
        key: int,
        code: int,
        state: Gdk.ModifierType,
    ) -> None:
        self._is_pressed_by_combo = {}
        self._message(Action.IDLE, 0)

    def _message(self, action: Action, value: float) -> None:
        # Talk back to the service in the right context
        add_idle_source(self._service.message, (action, value), self._context)

    def shutdown(self) -> None:
        self._is_pressed_by_combo = {}

        if self._key_pressed_source_id is not None:
            self.disconnect(self._key_pressed_source_id)
        if self._key_released_source_id is not None:
            self.disconnect(self._key_released_source_id)
        if self._registered_source_id is not None:
            self._service.disconnect(self._registered_source_id)

        self._widget.remove_controller(self)

        logger.debug("Client.Keyboard.shut")
