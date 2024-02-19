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

from typing import Dict, Optional

from gi.repository import GLib, GObject

from .scene import Scene
from .entity import Entity

from ..network.tcp import Server as TCPServer
from ..network.tcp import Client as TCPClient

from ...common.vector import Vector
from ...common.scanner import Description
from ...common.utils import get_project_path
from ...common.logger import logger
from ...common.session import Session as CommonSession
from ...common.scene import SceneRequest as CommonSceneRequest
from ...common.stats import StatsRequest as CommonStatsRequest
from ...common.message import Message as CommonMessage
from ...common.dialogue import Dialogue as CommonDialogue
from ...common.payload import Payload
from ...common.errors import Error
from ...common.config import VERSION
from ...common.utils import get_project_name


class Session(CommonSession):
    def __init__(
        self,
        id: int,
        error: Optional[int],
        entity_id: int,
        client: TCPClient,
        sequence: int = -1,
    ) -> None:
        super().__init__(id=id, entity_id=entity_id, error=error)
        self.client = client
        self.sequence = sequence


class Service(GObject.GObject):
    __gsignals__ = {
        "registered": (GObject.SignalFlags.RUN_LAST, None, (object,)),
        "updated": (GObject.SignalFlags.RUN_LAST, None, ()),
        "unregistered": (GObject.SignalFlags.RUN_LAST, None, (object,)),
    }

    def __init__(
        self,
        scene: str,
        clients: int,
        session_port: int,
        messages_port: int,
        context: GLib.MainContext,
    ) -> None:
        super().__init__()

        self._index = 0
        self._session_by_client: Dict[TCPClient, Session] = {}
        self._session_by_id: Dict[int, Session] = {}
        self._session_by_entity_id: Dict[int, Session] = {}

        self.scene = Scene.new_from_description(
            Description.new_from_json(
                get_project_path(scene),
            )
        )

        self._session_manager = TCPServer(
            port=session_port,
            clients=clients,
            context=context,
        )
        self._session_manager.connect("connected", self.__on_session_connected)
        self._session_manager.connect("received", self.__on_session_received)
        self._session_manager.connect("disconnected", self.__on_session_disconnected)

        logger.debug("Server.Service.Started")

    def __on_session_connected(
        self,
        manager: TCPServer,
        client: TCPClient,
        data: str,
    ) -> None:
        request = Payload.deserialize(data).session_request

        if request.version != VERSION:
            client.send(
                Payload(
                    session=CommonSession(
                        id=-1,
                        entity_id=-1,
                        error=Error.VERSION,
                    )
                ).serialize()
            )
            return

        if request.project != get_project_name():
            client.send(
                Payload(
                    session=CommonSession(
                        id=-1,
                        entity_id=-1,
                        error=Error.PROJECT,
                    )
                ).serialize()
            )
            return

        entity = self.scene.add(
            request.type_id,
            position=Vector(
                x=self.scene.spawn.x,
                y=self.scene.spawn.y,
                z=self.scene.spawn.z,
            ),
            overrides=Description(
                name=request.username,
            ),
            playable=True,
        )
        entity.connect("told", self.__on_entity_told)

        session = Session(
            id=self._index,
            error=None,
            entity_id=entity.id,
            client=client,
        )

        self._index += 1
        self._session_by_client[client] = session
        self._session_by_id[session.id] = session
        self._session_by_entity_id[entity.id] = session

        client.send(Payload(session=session).serialize())

        self.emit("registered", session)

        logger.debug("Server.Service.Registered %s", client)

    def __on_session_received(
        self,
        manager: TCPServer,
        client: TCPClient,
        data: str,
    ) -> None:
        payload = Payload.deserialize(data)

        if payload.message is not None:
            self.__on_message_received(payload.message)
        elif payload.scene_request is not None:
            self.__on_scene_requested(payload.scene_request, client)
        elif payload.stats_request is not None:
            self.__on_stats_requested(payload.stats_request, client)

    def __on_session_disconnected(
        self,
        manager: TCPServer,
        client: TCPClient,
    ) -> None:
        session = self._session_by_client.get(client)

        if session is None:
            return

        self.scene.remove(session.entity_id)

        del self._session_by_client[client]
        del self._session_by_entity_id[session.entity_id]
        del self._session_by_id[session.id]

        self.emit("unregistered", session)
        client.shutdown()

        logger.debug("Server.Service.Unregistered %s", client)

    def __on_entity_told(self, entity: Entity, text: str) -> None:
        client = self._session_by_entity_id[entity.id].client
        client.send(Payload(dialogue=CommonDialogue(text=text)).serialize())

    def __on_message_received(
        self,
        message: CommonMessage,
    ) -> None:
        session = self._session_by_id.get(message.session_id)

        if session is None:
            return
        if message.sequence < session.sequence:
            return

        session.sequence = message.sequence
        self.scene.update(session.entity_id, message.action, message.value)
        self.emit("updated")

    def __on_scene_requested(
        self,
        request: CommonSceneRequest,
        client: TCPClient,
    ) -> None:
        session = self._session_by_id.get(request.session_id)

        if session is None:
            return

        scene = self.scene.prepare_for_entity_id(session.entity_id)
        client.send(Payload(scene=scene).serialize())

    def __on_stats_requested(
        self,
        request: CommonStatsRequest,
        client: TCPClient,
    ) -> None:
        session = self._session_by_id.get(request.session_id)

        if session is None:
            return

        stats = self.scene.prepare_stats_for_entity_id(session.entity_id)
        client.send(Payload(stats=stats).serialize())

    def shutdown(self) -> None:
        self.scene.shutdown()
        self._session_manager.shutdown()

        logger.debug("Server.Service.shut")
