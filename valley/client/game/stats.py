from gi.repository import GObject, GLib

from .service import Service

from ...common.session import Session
from ...common.stats import Stats as CommonStats


class Scene(CommonStats, GObject.GObject):
    __gsignals__ = {
        "updated": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    def __init__(self, service: Service) -> None:
        CommonStats.__init__(self)
        GObject.GObject.__init__(self)

        self._service = service
        self._service.connect("registered", self.__on_service_registered)

    def __on_service_registered(self, service: Service, session: Session) -> None:
        self._service.connect("stats-updated", self.__on_service_updated)
        GLib.timeout_add_seconds(1, self.__on_scene_ticked)

    def __on_service_updated(self, service: Service, stats: CommonStats) -> None:
        self.durability = stats.durability
        self.stamina = stats.stamina
        self.held = stats.held

        self.emit("updated")
