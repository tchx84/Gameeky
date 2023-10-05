from .scene import Scene

from ..network.tcp import Server as TCPServer
from ..network.udp import Server as UDPServer

from ...common.heartbeat import Heartbeat
from ...common.session import Session as CommonSession
from ...common.message import Message


class Session(CommonSession):
    def __init__(self, id, client, entity_id, sequence=-1):
        super().__init__(id)
        self._client = client
        self._entity_id = entity_id
        self._sequence = sequence

    @property
    def entity_id(self):
        return self._entity_id

    @property
    def sequence(self):
        return self._sequence

    @sequence.setter
    def sequence(self, sequence):
        self._sequence = sequence


class Service(object):
    def __init__(self, clients, session_port, updates_port, scene_port, context):
        self._sessions = 0
        self._session_by_client = {}
        self._session_by_id = {}

        self.scene = Scene()

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
        session = Session(id=self._sessions, client=client, entity_id=entity_id)

        self._session_by_client[client] = session
        self._session_by_id[session.id] = session
        self._sessions += 1

        client.send(session.serialize())

    def __on_session_disconnected(self, manager, client):
        session = self._session_by_client.get(client)

        self.scene.remove(session.entity_id)

        del self._session_by_client[client]
        del self._session_by_id[session.id]

    def __on_message_received(self, manager, address, data):
        message = Message.deserialize(data)
        session = self._session_by_id.get(message.session_id)

        if session is None:
            return
        if message.sequence < session.sequence:
            return

        session.sequence = message.sequence
        self.scene.qeueu(session.entity_id, message.action)

    def __on_scene_requested(self, manager, address, data):
        heartbeat = Heartbeat.deserialize(data)

        if self._session_by_id.get(heartbeat.session_id) is None:
            return

        # XXX prepare scene specifically for session.entities_ids
        self._scene_manager.send(address, self.scene.serialize())
