from typing import Tuple

from gi.repository import GLib

from .serializeable import Serializeable


class Heartbeat(Serializeable):
    SIGNATURE = "(i)"

    def __init__(self, session_id: int) -> None:
        self.session_id = session_id

    def to_variant(self) -> GLib.Variant:
        return GLib.Variant(self.SIGNATURE, (self.session_id,))

    @classmethod
    def from_values(cls, values: Tuple[int]) -> "Heartbeat":
        return cls(*values)
