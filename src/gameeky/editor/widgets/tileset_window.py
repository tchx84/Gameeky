from gi.repository import Gtk, Adw

from .tileset import Tileset


@Gtk.Template(resource_path="/dev/tchx84/gameeky/editor/widgets/tileset_window.ui")  # fmt: skip
class TilesetWindow(Adw.Window):
    __gtype_name__ = "TilesetWindow"

    tile_box = Gtk.Template.Child()

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)

        self._tileset = Tileset()
        self.tile_box.append(self._tileset)

    @Gtk.Template.Callback("on_zoom_in")
    def __on_soom_in(self, button: Gtk.Button) -> None:
        self._tileset.scale += 0.1

    @Gtk.Template.Callback("on_zoom_out")
    def __on_soom_out(self, button: Gtk.Button) -> None:
        self._tileset.scale -= 0.1

    @property
    def rows(self) -> int:
        return self._tileset.rows

    @rows.setter
    def rows(self, rows: int) -> None:
        self._tileset.rows = rows

    @property
    def columns(self) -> int:
        return self._tileset.columns

    @columns.setter
    def columns(self, columns: int) -> None:
        self._tileset.columns = columns

    @property
    def path(self) -> str:
        return self._tileset.path

    @path.setter
    def path(self, path: str) -> None:
        self._tileset.path = path
