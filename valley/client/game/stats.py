from typing import Optional
from gi.repository import GObject, GLib

from .service import Service

from ...common.session import Session
from ...common.stats import Stats as CommonStats


class Stats(CommonStats, GObject.GObject):
    __gsignals__ = {
        "updated": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    def __init__(self, service: Service) -> None:
        CommonStats.__init__(self)
        GObject.GObject.__init__(self)
        self._timeout_handler_id: Optional[int] = None

        self._service = service
        self._service.connect("stats-updated", self.__on_service_updated)
        self._service.connect("registered", self.__on_service_registered)

    def __on_service_registered(self, service: Service, session: Session) -> None:
        self._timeout_handler_id = GLib.timeout_add_seconds(1, self.__on_stats_ticked)

    def __on_stats_ticked(self) -> int:
        self._service.request_stats()
        return GLib.SOURCE_CONTINUE

    def __on_service_updated(self, service: Service, stats: CommonStats) -> None:
        self.durability = stats.durability
        self.stamina = stats.stamina
        self.held = stats.held

        self.emit("updated")

    def shutdown_timeout(self) -> None:
        if self._timeout_handler_id is None:
            return

        GLib.Source.remove(self._timeout_handler_id)
        self._timeout_handler_id = None

    def shutdown(self) -> None:
        self.shutdown_timeout()
        self._service.disconnect_by_func(self.__on_service_updated)
        self._service.disconnect_by_func(self.__on_service_registered)
