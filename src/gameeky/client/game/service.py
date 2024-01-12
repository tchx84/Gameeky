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

from gi.repository import Gio, GLib, GObject

from ..network.tcp import Client as TCPClient
from ..network.udp import Client as UDPClient

from ...common.logger import logger
from ...common.definitions import Action, EntityType
from ...common.scene import SceneRequest
from ...common.session import SessionRequest
from ...common.stats import StatsRequest
from ...common.message import Message
from ...common.payload import Payload
from ...common.errors import Error
from ...common.config import VERSION
from ...common.utils import get_project_name


class Service(GObject.GObject):
    __gsignals__ = {
        "registered": (GObject.SignalFlags.RUN_LAST, None, (object,)),
        "scene-updated": (GObject.SignalFlags.RUN_LAST, None, (object,)),
        "stats-updated": (GObject.SignalFlags.RUN_LAST, None, (object,)),
        "failed": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    def __init__(
        self,
        address: str,
        session_port: int,
        messages_port: int,
        context: GLib.MainContext,
    ) -> None:
        super().__init__()

        self._sequence = 0

        self._session_manager = TCPClient(
            address=address,
            port=session_port,
            context=context,
        )
        self._messages_manager = UDPClient(
            address=address,
            port=messages_port,
            context=context,
        )

        self._session_manager.connect("received", self.__on_session_registered)
        self._session_manager.connect("failed", self.__on_session_failed)

    def __on_session_registered(self, client: TCPClient, data: bytes) -> None:
        session = Payload.deserialize(data).session

        if session.error is not None:
            logger.error(Error.describe(session.error))
            self.emit("failed")
            return

        self._session = session
        self._messages_manager.connect("received", self.__on_payload_received)
        self.emit("registered", self._session)

    def __on_session_failed(self, client: TCPClient) -> None:
        self.emit("failed")

    def __on_payload_received(
        self,
        manager: UDPClient,
        address: Gio.InetSocketAddress,
        data: bytes,
    ) -> None:
        payload = Payload.deserialize(data)

        if payload.scene is not None:
            self.emit("scene-updated", payload.scene)
        elif payload.stats is not None:
            self.emit("stats-updated", payload.stats)

    def register(self) -> None:
        self._session_manager.send(
            Payload(
                session_request=SessionRequest(
                    type_id=EntityType.PLAYER,
                    version=VERSION,
                    project=get_project_name(),
                )
            ).serialize()
        )

    def unregister(self) -> None:
        self._messages_manager.shutdown()
        self._session_manager.shutdown()

        logger.debug("Client.Service.shut")

    def message(self, action: Action, value: float) -> None:
        self._messages_manager.send(
            Payload(
                message=Message(
                    self._session.id,
                    action,
                    value,
                    self._sequence,
                )
            ).serialize()
        )
        self._sequence += 1

    def request_scene(self) -> None:
        self._messages_manager.send(
            Payload(scene_request=SceneRequest(self._session.id)).serialize()
        )

    def request_stats(self) -> None:
        self._messages_manager.send(
            Payload(stats_request=StatsRequest(self._session.id)).serialize()
        )
