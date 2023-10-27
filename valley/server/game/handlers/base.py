from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..entity import Entity

from ....common.utils import get_time_milliseconds


class Handler:
    def __init__(self, entity: Entity) -> None:
        self.busy = False

        self._entity = entity

        timestamp = get_time_milliseconds()
        self._timestamp_prepare = timestamp
        self._timestamp_tick = timestamp
        self._timestamp_finish = timestamp

    def _get_elapsed_seconds_since_tick(self) -> float:
        return (get_time_milliseconds() - self._timestamp_tick) / 1000

    def _get_elapsed_seconds_since_prepare(self) -> float:
        return (get_time_milliseconds() - self._timestamp_prepare) / 1000

    def _get_elapsed_seconds_since_finish(self) -> float:
        return (get_time_milliseconds() - self._timestamp_finish) / 1000

    def prepare(self, value: float) -> bool:
        self.busy = True
        self._timestamp_prepare = get_time_milliseconds()
        self._timestamp_tick = get_time_milliseconds()

        return True

    def tick(self) -> None:
        self._timestamp_tick = get_time_milliseconds()

    def finish(self) -> None:
        self.busy = False
        self._timestamp_finish = get_time_milliseconds()

    def cancel(self) -> None:
        self.finish()
