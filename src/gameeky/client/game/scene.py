import math

from typing import Optional
from gi.repository import GObject, GLib

from .service import Service

from ...common.logger import logger
from ...common.definitions import TICK
from ...common.session import Session
from ...common.scene import Scene as CommonScene
from ...common.utils import add_timeout_source, remove_source_id


class Scene(CommonScene, GObject.GObject):
    __gsignals__ = {
        "ticked": (GObject.SignalFlags.RUN_LAST, None, ()),
        "updated": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    def __init__(self, width: int, height: int, service: Service) -> None:
        CommonScene.__init__(self, width, height)
        GObject.GObject.__init__(self)
        self._service = service

        self._timeout_source_id: Optional[int] = None
        self._updated_source_id: Optional[int] = None
        self._registered_source_id: Optional[int] = self._service.connect(
            "registered",
            self.__on_service_registered,
        )

    def __on_service_registered(self, service: Service, session: Session) -> None:
        self._updated_source_id = self._service.connect(
            "scene-updated",
            self.__on_service_updated,
        )
        self._timeout_source_id = add_timeout_source(
            TICK,
            self.__on_scene_ticked,
        )

    def __on_service_updated(self, service: Service, scene: CommonScene) -> None:
        # Take z-depth into account
        scene.entities = sorted(
            scene.entities,
            key=lambda e: (
                math.ceil(e.position.y),
                e.position.z,
                math.ceil(e.position.x),
            ),
        )

        GLib.idle_add(self._update_on_main_thread, scene)

    def _update_on_main_thread(self, scene: CommonScene) -> None:
        self.time = scene.time
        self.anchor = scene.anchor
        self.entities = scene.entities

        self.emit("updated")

    def __on_scene_ticked(self, *args) -> int:
        self._service.request_scene()
        self.emit("ticked")
        return GLib.SOURCE_CONTINUE

    def shutdown(self) -> None:
        if self._timeout_source_id is not None:
            remove_source_id(self._timeout_source_id)

        if self._updated_source_id is not None:
            self._service.disconnect(self._updated_source_id)

        if self._registered_source_id is not None:
            self._service.disconnect(self._registered_source_id)

        self._timeout_source_id = None
        self._updated_source_id = None
        self._registered_source_id = None

        logger.debug("Client.Scene.shut")
