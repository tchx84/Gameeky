from typing import Dict

from gi.repository import GLib, GObject

from .scene import Scene

from ..network.tcp import Server as TCPServer
from ..network.tcp import Client as TCPClient
from ..network.udp import Server as UDPServer

from ...common.vector import Vector
from ...common.scanner import Description
from ...common.utils import get_data_path
from ...common.logger import logger
from ...common.scene import SceneRequest
from ...common.stats import StatsRequest
from ...common.session import SessionRequest
from ...common.session import Session as CommonSession
from ...common.message import Message


class Session(CommonSession):
    def __init__(self, id, entity_id: int, sequence: int = -1) -> None:
        super().__init__(id=id)
        self.entity_id = entity_id
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
        scene_port: int,
        stats_port: int,
        context: GLib.MainContext,
    ) -> None:
        super().__init__()

        self._index = 0
        self._session_by_client: Dict[TCPClient, Session] = {}
        self._session_by_id: Dict[int, Session] = {}

        self.scene = Scene.new_from_description(
            Description.new_from_json(
                get_data_path(scene),
            )
        )

        self._session_manager = TCPServer(
            port=session_port,
            clients=clients,
            context=context,
        )
        self._session_manager.connect("connected", self.__on_session_connected)
        self._session_manager.connect("disconnected", self.__on_session_disconnected)

        self._messages_manager = UDPServer(port=messages_port, context=context)
        self._messages_manager.connect("received", self.__on_message_received)

        self._scene_manager = UDPServer(port=scene_port, context=context)
        self._scene_manager.connect("received", self.__on_scene_requested)

        self._stats_manager = UDPServer(port=stats_port, context=context)
        self._stats_manager.connect("received", self.__on_stats_requested)

        logger.debug("Server.Service.Started")

    def __on_session_connected(self, manager, client, data):
        request = SessionRequest.deserialize(data)

        entity_id = self.scene.add(
            request.type_id,
            position=Vector(
                x=self.scene.spawn.x,
                y=self.scene.spawn.y,
                z=self.scene.spawn.z,
            ),
        )

        session = Session(id=self._index, entity_id=entity_id)

        self._index += 1
        self._session_by_client[client] = session
        self._session_by_id[session.id] = session

        client.send(session.serialize())

        self.emit("registered", session)

        logger.debug("Server.Service.Registered %s", client)

    def __on_session_disconnected(self, manager, client):
        session = self._session_by_client.get(client)

        if session is None:
            return

        self.scene.remove(session.entity_id)

        del self._session_by_client[client]
        del self._session_by_id[session.id]

        self.emit("unregistered", session)

        logger.debug("Server.Service.Unregistered %s", client)

    def __on_message_received(self, manager, address, data):
        message = Message.deserialize(data)
        session = self._session_by_id.get(message.session_id)

        if session is None:
            return
        if message.sequence < session.sequence:
            return

        session.sequence = message.sequence
        self.scene.update(session.entity_id, message.action, message.value)
        self.emit("updated")

    def __on_scene_requested(self, manager, address, data):
        request = SceneRequest.deserialize(data)
        session = self._session_by_id.get(request.session_id)

        if session is None:
            return

        scene = self.scene.prepare_for_entity_id(session.entity_id)
        self._scene_manager.send(address, scene.serialize())

    def __on_stats_requested(self, manager, address, data):
        request = StatsRequest.deserialize(data)
        session = self._session_by_id.get(request.session_id)

        if session is None:
            return

        stats = self.scene.prepare_stats_for_entity_id(session.entity_id)
        self._stats_manager.send(address, stats.serialize())

    def shutdown(self) -> None:
        self.scene.shutdown()
        self._stats_manager.shutdown()
        self._scene_manager.shutdown()
        self._messages_manager.shutdown()
        self._session_manager.shutdown()

        logger.debug("Server.Service.shut")
