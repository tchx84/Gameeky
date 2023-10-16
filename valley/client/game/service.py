from gi.repository import Gio, GLib, GObject

from ..network.tcp import Client as TCPClient
from ..network.udp import Client as UDPClient

from ...common.action import Action
from ...common.scene import Scene, SceneRequest
from ...common.session import Session, SessionRequest
from ...common.message import Message


class Service(GObject.GObject):
    __gsignals__ = {
        "registered": (GObject.SignalFlags.RUN_LAST, None, (object,)),
        "updated": (GObject.SignalFlags.RUN_LAST, None, (object,)),
    }

    def __init__(
        self,
        address: str,
        session_port: int,
        messages_port: int,
        scene_port: int,
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
        self._scene_manager = UDPClient(
            address=address,
            port=scene_port,
            context=context,
        )

        self._session_manager.connect("received", self.__on_session_registered)

    def __on_session_registered(self, client: TCPClient, data: bytes) -> None:
        self._session = Session.deserialize(data)
        self._scene_manager.connect("received", self.__on_scene_received)
        self.emit("registered", self._session)

    def __on_scene_received(
        self,
        manager: UDPClient,
        address: Gio.InetSocketAddress,
        data: bytes,
    ) -> None:
        self.emit("updated", Scene.deserialize(data))

    def register(self) -> None:
        self._session_manager.send(SessionRequest(type_id=1).serialize())

    def unregister(self) -> None:
        self._session_manager.shutdown()

    def message(self, action: Action, value: float) -> None:
        self._messages_manager.send(
            Message(
                self._session.id,
                action,
                value,
                self._sequence,
            ).serialize()
        )
        self._sequence += 1

    def request(self) -> None:
        self._scene_manager.send(SceneRequest(self._session.id).serialize())
