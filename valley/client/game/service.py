from gi.repository import GObject

from ..network.tcp import Client as TCPClient
from ..network.udp import Client as UDPClient

from ...common.scene import Scene, SceneRequest
from ...common.session import Session, SessionRequest
from ...common.message import Message


class Service(GObject.GObject):
    __gsignals__ = {
        "registered": (GObject.SignalFlags.RUN_LAST, None, (object,)),
        "updated": (GObject.SignalFlags.RUN_LAST, None, (object,)),
    }

    def __init__(self, address, session_port, messages_port, scene_port, context):
        super().__init__()

        self._sequence = 0
        self._session = None

        self._session_manager = TCPClient(
            address=address, port=session_port, context=context
        )
        self._session_manager.connect("received", self.__on_session_registered)

        self._messages_manager = UDPClient(
            address=address, port=messages_port, context=context
        )

        self._scene_manager = UDPClient(
            address=address, port=scene_port, context=context
        )
        self._scene_manager.connect("received", self.__on_scene_received)

    def __on_session_registered(self, client, data):
        self._session = Session.deserialize(data)
        self.emit("registered", self._session)

    def __on_scene_received(self, manager, address, data):
        self.emit("updated", Scene.deserialize(data))

    def register(self):
        self._session_manager.send(SessionRequest().serialize())

    def unregister(self):
        self._session_manager.close()

    def report(self, action, value):
        self._messages_manager.send(
            Message(self._session.id, action, value, self._sequence).serialize()
        )
        self._sequence += 1

    def request(self):
        self._scene_manager.send(SceneRequest(self._session.id).serialize())
