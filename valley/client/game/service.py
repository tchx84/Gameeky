from gi.repository import Gio, GLib, GObject

from ..network.tcp import Client as TCPClient
from ..network.udp import Client as UDPClient

from ...common.definitions import Action, EntityType
from ...common.scene import Scene, SceneRequest
from ...common.session import Session, SessionRequest
from ...common.stats import Stats, StatsRequest
from ...common.message import Message


class Service(GObject.GObject):
    __gsignals__ = {
        "registered": (GObject.SignalFlags.RUN_LAST, None, (object,)),
        "scene-updated": (GObject.SignalFlags.RUN_LAST, None, (object,)),
        "stats-updated": (GObject.SignalFlags.RUN_LAST, None, (object,)),
    }

    def __init__(
        self,
        address: str,
        session_port: int,
        messages_port: int,
        scene_port: int,
        stats_port: int,
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
        self._stats_manager = UDPClient(
            address=address,
            port=stats_port,
            context=context,
        )

        self._session_manager.connect("received", self.__on_session_registered)

    def __on_session_registered(self, client: TCPClient, data: bytes) -> None:
        self._session = Session.deserialize(data)
        self._scene_manager.connect("received", self.__on_scene_received)
        self._stats_manager.connect("received", self.__on_stats_received)
        self.emit("registered", self._session)

    def __on_stats_received(
        self,
        manager: UDPClient,
        address: Gio.InetSocketAddress,
        data: bytes,
    ) -> None:
        self.emit("stats-updated", Stats.deserialize(data))

    def __on_scene_received(
        self,
        manager: UDPClient,
        address: Gio.InetSocketAddress,
        data: bytes,
    ) -> None:
        self.emit("scene-updated", Scene.deserialize(data))

    def register(self) -> None:
        self._session_manager.send(
            SessionRequest(
                type_id=EntityType.PLAYER,
            ).serialize()
        )

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

    def request_scene(self) -> None:
        self._scene_manager.send(SceneRequest(self._session.id).serialize())

    def request_stats(self) -> None:
        self._stats_manager.send(StatsRequest(self._session.id).serialize())
