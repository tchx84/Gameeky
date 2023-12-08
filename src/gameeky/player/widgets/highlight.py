from gi.repository import Gtk

from ...client.graphics.highlight import Highlight as HighlightGraphics

from ...common.definitions import TILES_X, TILES_Y


class Highlight(Gtk.AspectFrame):
    def __init__(self) -> None:
        super().__init__()

        self._view = HighlightGraphics()
        self._view.set_vexpand(True)
        self._view.set_hexpand(True)

        self.set_obey_child(False)
        self.set_ratio(TILES_X / TILES_Y)
        self.set_child(self._view)

    @property
    def canvas(self) -> Gtk.Widget:
        return self._view
