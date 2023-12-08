from gi.repository import Gtk


def present_about(window: Gtk.Window) -> None:
    builder = Gtk.Builder.new_from_resource("/dev/tchx84/gameeky/common/widgets/about_window.ui")  # fmt: skip
    dialog = builder.get_object("AboutWindow")
    dialog.props.transient_for = window
    dialog.present()
