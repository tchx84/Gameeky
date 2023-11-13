import os

__dir__ = os.path.dirname(os.path.abspath(__file__))

from gi.repository import Gtk, Adw


@Gtk.Template(filename=os.path.join(__dir__, "scene_window.ui"))
class SceneWindow(Adw.ApplicationWindow):
    __gtype_name__ = "SceneWindow"
