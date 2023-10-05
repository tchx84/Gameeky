from typing import Any

from gi.repository import GLib


class Serializeable(object):
    SIGNATURE = ""

    def to_variant(self) -> GLib.Variant:
        raise NotImplementedError

    @classmethod
    def from_values(cls, values: Any) -> Any:
        raise NotImplementedError

    def serialize(self) -> bytes:
        return self.to_variant().get_data_as_bytes().get_data()

    @classmethod
    def deserialize(cls, data: bytes) -> Any:
        values = GLib.Variant.new_from_bytes(
            GLib.VariantType(cls.SIGNATURE), GLib.Bytes(data), True
        ).unpack()

        return cls.from_values(values)
