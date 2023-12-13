from typing import Optional
from gi.repository import GObject, GLib

from .service import Service

from ...common.logger import logger
from ...common.session import Session
from ...common.stats import Stats as CommonStats
from ...common.utils import add_timeout_source, remove_source_id


class Stats(CommonStats, GObject.GObject):
    __gsignals__ = {
        "updated": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    def __init__(self, service: Service) -> None:
        CommonStats.__init__(self)
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
            "stats-updated",
            self.__on_service_updated,
        )
        self._timeout_source_id = add_timeout_source(
            1000,
            self.__on_stats_ticked,
        )

    def __on_stats_ticked(self, *args) -> int:
        self._service.request_stats()
        return GLib.SOURCE_CONTINUE

    def __on_service_updated(self, service: Service, stats: CommonStats) -> None:
        GLib.idle_add(self._update_on_main_thread, stats)

    def _update_on_main_thread(self, stats: CommonStats) -> None:
        self.durability = stats.durability
        self.stamina = stats.stamina
        self.held = stats.held

        self.emit("updated")

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

        logger.debug("Client.Stats.shut")
