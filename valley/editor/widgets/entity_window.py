import os

__dir__ = os.path.dirname(os.path.abspath(__file__))

from gi.repository import Gtk, Adw

from .global_settings import GlobalSettings
from .entity_settings import EntitySettings
from .animations_settings import AnimationsSettings
from .sounds_settings import SoundsSettings

from ...common.scanner import Description


@Gtk.Template(filename=os.path.join(__dir__, "entity_window.ui"))
class EntityWindow(Adw.ApplicationWindow):
    __gtype_name__ = "EntityWindow"

    game_box = Gtk.Template.Child()
    graphics_box = Gtk.Template.Child()
    sound_box = Gtk.Template.Child()

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self._global_settings = GlobalSettings()
        self._entity_settings = EntitySettings()
        self._animations_settings = AnimationsSettings()
        self._sounds_settings = SoundsSettings()

        self.game_box.append(self._global_settings)
        self.game_box.append(self._entity_settings)
        self.graphics_box.append(self._animations_settings)
        self.sound_box.append(self._sounds_settings)

    @property
    def suggested_name(self) -> str:
        prefix = f"{self._global_settings.description.id:04d}"
        suffix = f"{self._entity_settings.description.name.lower()}"

        return f"{prefix}_{suffix}.json"

    @property
    def description(self) -> Description:
        description = self._global_settings.description
        description.game.default = self._entity_settings.description
        description.graphics = self._animations_settings.description
        description.sound = self._sounds_settings.description

        return description

    @description.setter
    def description(self, description: Description) -> None:
        self._global_settings.description = description
        self._entity_settings.description = description.game.default
        self._animations_settings.description = description.graphics
        self._sounds_settings.description = description.sound
