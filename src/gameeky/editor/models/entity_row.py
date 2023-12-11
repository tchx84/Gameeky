from gi.repository import GObject


class EntityRow(GObject.GObject):
    __gtype_name__ = "EntityRowModel"

    type_id = GObject.Property(type=int)
    name = GObject.Property(type=str)

    def __init__(self, type_id: int, name: str, path: str) -> None:
        super().__init__()
        self.type_id = type_id
        self.name = name
        self.path = path
