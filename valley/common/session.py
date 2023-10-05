from typing import Tuple

from gi.repository import GLib

from .serializeable import Serializeable


class Session(Serializeable):
    SIGNATURE = "(ii)"

    def __init__(self, id: int, entity_id: int) -> None:
        self.id = id
        self.entity_id = entity_id

    def to_variant(self) -> GLib.Variant:
        return GLib.Variant(self.SIGNATURE, (self.id, self.entity_id))

    @classmethod
    def from_values(cls, values: Tuple[int, int]) -> "Session":
        return cls(*values)


class SessionRequest(Serializeable):
    SIGNATURE = "()"

    def __init__(self) -> None:
        pass

    def to_variant(self) -> GLib.Variant:
        return GLib.Variant(self.SIGNATURE, ())

    @classmethod
    def from_values(cls, values: Tuple) -> "SessionRequest":
        return cls()
