from gi.repository import GObject

from .scene import Scene

from ..network.tcp import Server as TCPServer
from ..network.udp import Server as UDPServer

from ...common.scene import SceneRequest
from ...common.session import Session as CommonSession
from ...common.message import Message
from ...common.definitions import TILE_SIZE


class Session(CommonSession):
    def __init__(self, id, entity_id, sequence=-1):
        super().__init__(id, entity_id)
        self.sequence = sequence


class Service(GObject.GObject):
    __gsignals__ = {
        "registered": (GObject.SignalFlags.RUN_LAST, None, (object,)),
        "unregistered": (GObject.SignalFlags.RUN_LAST, None, (object,)),
    }

    def __init__(self, clients, session_port, updates_port, scene_port, context):
        super().__init__()

        self._sessions = 0
        self._session_by_client = {}
        self._session_by_id = {}

        self.scene = Scene(width=TILE_SIZE, height=TILE_SIZE)

        self._session_manager = TCPServer(
            port=session_port, clients=clients, context=context
        )
        self._session_manager.connect("connected", self.__on_session_connected)
        self._session_manager.connect("disconnected", self.__on_session_disconnected)

        self._messages_manager = UDPServer(port=updates_port, context=context)
        self._messages_manager.connect("received", self.__on_message_received)

        self._scene_manager = UDPServer(port=scene_port, context=context)
        self._scene_manager.connect("received", self.__on_scene_requested)

    def __on_session_connected(self, manager, client, data):
        entity_id = self.scene.add()
        session = Session(id=self._sessions, entity_id=entity_id)

        self._session_by_client[client] = session
        self._session_by_id[session.id] = session
        self._sessions += 1

        client.send(session.serialize())

        self.emit("registered", session)

    def __on_session_disconnected(self, manager, client):
        session = self._session_by_client.get(client)

        if session is None:
            return

        self.scene.remove(session.entity_id)

        del self._session_by_client[client]
        del self._session_by_id[session.id]

        self.emit("unregistered", session)

    def __on_message_received(self, manager, address, data):
        message = Message.deserialize(data)
        session = self._session_by_id.get(message.session_id)

        if session is None:
            return
        if message.sequence < session.sequence:
            return

        session.sequence = message.sequence
        self.scene.update(session.entity_id, message.action, message.value)

    def __on_scene_requested(self, manager, address, data):
        request = SceneRequest.deserialize(data)
        session = self._session_by_id.get(request.session_id)

        if session is None:
            return

        scene = self.scene.prepare_for_entity_id(session.entity_id)
        self._scene_manager.send(address, scene.serialize())
