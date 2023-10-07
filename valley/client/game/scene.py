from gi.repository import GObject, GLib

from .service import Service

from ...common.definitions import TICK
from ...common.session import Session
from ...common.scene import Scene as CommonScene


class Scene(CommonScene, GObject.GObject):
    __gsignals__ = {
        "updated": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    def __init__(self, width, height, service: Service) -> None:
        CommonScene.__init__(self, width, height)
        GObject.GObject.__init__(self)

        self._service = service
        self._service.connect("registered", self.__on_service_registered)

    def __on_service_registered(self, service: Service, session: Session) -> None:
        self._service.connect("updated", self.__on_service_updated)
        GLib.timeout_add(TICK, self.__on_ticked)

    def __on_service_updated(self, service, scene):
        self.anchor = scene.anchor
        self.entities = scene.entities
        self.emit("updated")

    def __on_ticked(self):
        self._service.request()
        return GLib.SOURCE_CONTINUE
