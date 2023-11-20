import math

from typing import Optional
from gi.repository import GObject, GLib

from .service import Service

from ...common.definitions import TICK
from ...common.session import Session
from ...common.scene import Scene as CommonScene


class Scene(CommonScene, GObject.GObject):
    __gsignals__ = {
        "ticked": (GObject.SignalFlags.RUN_LAST, None, ()),
        "updated": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    def __init__(self, width: int, height: int, service: Service) -> None:
        CommonScene.__init__(self, width, height)
        GObject.GObject.__init__(self)
        self._timeout_handler_id: Optional[int] = None

        self._service = service
        self._service.connect("scene-updated", self.__on_service_updated)
        self._service.connect("registered", self.__on_service_registered)

    def __on_service_registered(self, service: Service, session: Session) -> None:
        self._timeout_handler_id = GLib.timeout_add(TICK, self.__on_scene_ticked)

    def __on_service_updated(self, service: Service, scene: CommonScene) -> None:
        self.time = scene.time
        self.anchor = scene.anchor

        # Take z-depth into account
        self.entities = sorted(
            scene.entities,
            key=lambda e: (
                math.ceil(e.position.y),
                e.position.z,
                math.ceil(e.position.x),
            ),
        )

        self.emit("updated")

    def __on_scene_ticked(self) -> int:
        self._service.request_scene()
        self.emit("ticked")
        return GLib.SOURCE_CONTINUE

    def shutdown_timeout(self) -> None:
        if self._timeout_handler_id is None:
            return

        GLib.Source.remove(self._timeout_handler_id)
        self._timeout_handler_id = None

    def shutdown(self) -> None:
        self.shutdown_timeout()
        self._service.disconnect_by_func(self.__on_service_updated)
        self._service.disconnect_by_func(self.__on_service_registered)
