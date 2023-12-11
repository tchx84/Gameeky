from gi.repository import Adw, Gtk, GObject


@Gtk.Template(resource_path="/dev/tchx84/gameeky/editor/widgets/confirmation_window.ui")  # fmt: skip
class ConfirmationWindow(Adw.MessageDialog):
    __gtype_name__ = "ConfirmationWindow"

    __gsignals__ = {
        "confirmed": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    @Gtk.Template.Callback("on_response_clicked")
    def __on_response_clicked(self, dialog, reponse: str) -> None:
        if reponse == "delete":
            self.emit("confirmed")
