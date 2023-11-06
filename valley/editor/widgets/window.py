import os

__dir__ = os.path.dirname(os.path.abspath(__file__))

from gi.repository import Gtk, Adw

from .animation import Animation
from .guide import Guide
from .entity import Entity


@Gtk.Template(filename=os.path.join(__dir__, "window.ui"))
class Window(Adw.ApplicationWindow):
    __gtype_name__ = "Window"

    content = Gtk.Template.Child()

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)

        self._animation = Animation()
        self._animation.props.hexpand = True
        self._animation.props.vexpand = True
        self._animation.connect("changed", self.__on_animation_changed)

        scrollable = Gtk.ScrolledWindow()
        scrollable.props.child = self._animation

        self._entity = Entity()
        self._entity.props.hexpand = True
        self._entity.props.vexpand = True

        self._guide = Guide()
        self._guide.props.hexpand = True
        self._guide.props.vexpand = True

        container = Gtk.Box()
        container.props.orientation = Gtk.Orientation.VERTICAL
        container.append(self._guide)
        container.append(self._entity)

        box = Gtk.Box()
        box.append(scrollable)
        box.append(container)

        self.content.append(box)

    def __on_animation_changed(self, animation: Animation) -> None:
        self._entity.update(animation.description)
        self._guide.update(animation.description)
