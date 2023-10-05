from typing import Tuple

from gi.repository import GLib

from .serializeable import Serializeable


class Session(Serializeable):
    SIGNATURE = "(i)"

    def __init__(self, id: int) -> None:
        self.id = id

    def to_variant(self) -> GLib.Variant:
        return GLib.Variant(self.SIGNATURE, (self.id,))

    @classmethod
    def from_values(cls, values: Tuple[int]) -> "Session":
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
