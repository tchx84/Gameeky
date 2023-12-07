import os

__dir__ = os.path.dirname(os.path.abspath(__file__))

from gi.repository import Gtk


def present_about(window: Gtk.Window) -> None:
    builder = Gtk.Builder.new_from_file(os.path.join(__dir__, "about_window.ui"))
    dialog = builder.get_object("AboutWindow")
    dialog.props.transient_for = window
    dialog.present()
