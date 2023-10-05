from gi.repository import GObject, GLib

from ...common.scene import Scene as CommonScene


class Scene(CommonScene, GObject.GObject):
    __gsignals__ = {
        "ticked": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    TICK = 100

    def __init__(self):
        CommonScene.__init__(self)
        GObject.GObject.__init__(self)
        GLib.timeout_add(self.TICK, self.__on_ticked)

    def update(self, scene: CommonScene):
        self.entities = scene.entities

    def __on_ticked(self):
        self.emit("ticked")
        return GLib.SOURCE_CONTINUE
