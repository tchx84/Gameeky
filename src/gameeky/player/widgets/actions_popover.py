from gi.repository import Gdk, Gtk, GObject

from ...common.definitions import Action


@Gtk.Template(resource_path="/dev/tchx84/gameeky/player/widgets/actions_popover.ui")  # fmt: skip
class ActionsPopover(Gtk.Popover):
    __gtype_name__ = "ActionsPopover"

    __gsignals__ = {
        "performed": (GObject.SignalFlags.RUN_LAST, None, (int,)),
    }

    def __init__(self, parent: Gtk.Widget) -> None:
        super().__init__()
        self.set_parent(parent)

    @Gtk.Template.Callback("on_activated")
    def __on_activated(self, box: Gtk.ListBox, row: Gtk.ListBoxRow) -> None:
        self.emit("performed", Action[row.props.name.upper()])
        self.popdown()

    def display(self, x: int, y: int) -> None:
        self.set_pointing_to(Gdk.Rectangle(x, y, 0, 0))
        self.set_offset(x, y)
        self.popup()
