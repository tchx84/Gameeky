# Copyright (c) 2023 Martín Abente Lahaye.
#
# This file is part of Gameeky
# (see gameeky.tchx84.dev).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from typing import Optional
from gi.repository import Gtk, Adw, GObject

from .scene import Scene as SceneWidget
from .hud import Hud as HudWidget
from .highlight import Highlight as HighlightWidget
from .actions_popover import ActionsPopover
from .dialogue import Dialogue

from ...client.game.scene import Scene as SceneModel
from ...client.game.stats import Stats as StatsModel
from ...client.game.dialogue import Dialogue as DialogueModel

from ...common.monitor import Monitor


@Gtk.Template(resource_path="/dev/tchx84/gameeky/player/widgets/window.ui")
class Window(Adw.ApplicationWindow):
    __gtype_name__ = "Window"

    __gsignals__ = {
        "reload": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    toast = Gtk.Template.Child()
    stack = Gtk.Template.Child()
    banner = Gtk.Template.Child()
    overlay = Gtk.Template.Child()

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self._scene = SceneWidget()
        self._hud = HudWidget()
        self._highlight = HighlightWidget()
        self._dialogue = Dialogue()

        self.overlay.add_overlay(self._scene)
        self.overlay.add_overlay(self._hud)
        self.overlay.add_overlay(self._highlight)
        self.overlay.add_overlay(self._dialogue)

        self._popover = ActionsPopover(parent=self.canvas)

        Monitor.default().connect("changed", self.__on_monitor_changed)

    def warn(self, title: str) -> None:
        toast = Adw.Toast()
        toast.props.title = title
        toast.props.timeout = 3

        self.toast.add_toast(toast)

    def switch_to_loading(self) -> None:
        self.stack.set_visible_child_name("loading")

    def switch_to_failed(self) -> None:
        self.stack.set_visible_child_name("failed")

    def switch_to_game(self) -> None:
        self.stack.set_visible_child_name("game")

    def __on_monitor_changed(self, monitor: Monitor) -> None:
        self.banner.props.revealed = True

    @Gtk.Template.Callback("on_reload_clicked")
    def __on_reload_clicked(self, button: Gtk.Button) -> None:
        self.banner.props.revealed = False
        self.emit("reload")

    @property
    def scene(self) -> Optional[SceneModel]:
        return self._scene.model

    @scene.setter
    def scene(self, scene: Optional[SceneModel]) -> None:
        self._scene.model = scene

    @property
    def stats(self) -> Optional[StatsModel]:
        return self._hud.model

    @stats.setter
    def stats(self, stats: Optional[StatsModel]) -> None:
        self._hud.model = stats

    @property
    def dialogue(self) -> Optional[DialogueModel]:
        return self._dialogue.model

    @dialogue.setter
    def dialogue(self, dialogue: Optional[DialogueModel]) -> None:
        self._dialogue.model = dialogue

    @property
    def canvas(self) -> Gtk.Widget:
        return self._highlight.canvas

    @property
    def popover(self) -> ActionsPopover:
        return self._popover
