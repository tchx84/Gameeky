from gi.repository import GObject, GLib

from ...common.definitions import TICK
from ...common.scene import Scene as CommonScene


class Scene(CommonScene, GObject.GObject):
    __gsignals__ = {
        "ticked": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    def __init__(self, width, height):
        CommonScene.__init__(self, width, height)
        GObject.GObject.__init__(self)

        GLib.timeout_add(TICK, self.__on_ticked)

    def update(self, scene: CommonScene):
        self.anchor = scene.anchor
        self.entities = scene.entities

    def __on_ticked(self):
        self.emit("ticked")
        return GLib.SOURCE_CONTINUE
